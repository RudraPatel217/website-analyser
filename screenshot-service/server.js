const express = require('express');
const puppeteer = require('puppeteer');
const rateLimit = require('express-rate-limit');
const dns = require('dns').promises;
const { URL } = require('url');

const app = express();

// Enable trust proxy for accurate IP identification
app.set('trust proxy', true);

// Security: Enforce rate limiting to prevent DoS attacks, while skipping local loopback
const limiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute window
  max: 60, // Limit each IP to 60 requests per minute
  standardHeaders: true,
  legacyHeaders: false,
  skip: (req) => {
    const ip = req.ip || req.connection.remoteAddress || '';
    return ip === '127.0.0.1' || ip === '::1' || ip === '::ffff:127.0.0.1' || ip === 'localhost';
  },
  message: { error: 'Too many screenshot requests from this IP, please try again after a minute.' }
});

app.use('/screenshot', limiter);

// Concurrency & Queue Control
let activeBrowsers = 0;
const MAX_CONCURRENT_BROWSERS = 3;
const requestQueue = [];

/**
 * Process next request waiting in the concurrency queue
 */
function processQueue() {
  if (activeBrowsers >= MAX_CONCURRENT_BROWSERS || requestQueue.length === 0) {
    return;
  }
  const nextReq = requestQueue.shift();
  if (nextReq) {
    nextReq();
  }
}

/**
 * Acquire a browser slot (waits in queue if max concurrent is reached)
 */
function acquireSlot(timeoutMs = 15000) {
  return new Promise((resolve, reject) => {
    if (activeBrowsers < MAX_CONCURRENT_BROWSERS) {
      activeBrowsers++;
      return resolve();
    }

    const timer = setTimeout(() => {
      const idx = requestQueue.indexOf(run);
      if (idx !== -1) {
        requestQueue.splice(idx, 1);
      }
      reject(new Error('Screenshot queue timeout. Maximum server capacity reached, please try again.'));
    }, timeoutMs);

    function run() {
      clearTimeout(timer);
      activeBrowsers++;
      resolve();
    }

    requestQueue.push(run);
  });
}

function releaseSlot() {
  activeBrowsers = Math.max(0, activeBrowsers - 1);
  processQueue();
}

/**
 * SSRF Validator: Ensures requested target is a public domain/IP.
 */
async function validateUrlSafety(inputUrl) {
  try {
    const parsed = new URL(inputUrl);
    
    // 1. Scheme Check: Only allow http and https
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
      return { safe: false, reason: 'Only HTTP and HTTPS protocols are permitted.' };
    }
    
    const hostname = parsed.hostname.toLowerCase().trim();
    
    // 2. Explicit Hostname Blocklist
    const blockedHosts = ['localhost', '127.0.0.1', '0.0.0.0', '::1', '169.254.169.254'];
    if (blockedHosts.includes(hostname)) {
      return { safe: false, reason: 'Access to loopback, internal network, or metadata endpoints is forbidden (SSRF Protection).' };
    }
    
    // 3. Resolve DNS IP addresses and check against private subnets
    const addresses = await dns.lookup(hostname, { all: true });
    for (const addr of addresses) {
      const ip = addr.address;
      if (isPrivateIp(ip)) {
        return { safe: false, reason: `Target resolves to private network IP address (${ip}). Request blocked for SSRF protection.` };
      }
    }
    
    return { safe: true, url: parsed.href };
  } catch (err) {
    return { safe: false, reason: 'Invalid or unresolvable URL provided.' };
  }
}

/**
 * Helper to test if an IPv4/IPv6 address falls into private/loopback ranges
 */
function isPrivateIp(ip) {
  if (!ip || typeof ip !== 'string') return true;
  
  if (ip === '::1' || ip.startsWith('fe80:') || ip.startsWith('fc00:')) return true;
  if (ip.startsWith('::ffff:')) {
    ip = ip.replace('::ffff:', '');
  }
  
  const parts = ip.split('.').map(Number);
  if (parts.length !== 4 || parts.some(isNaN)) return false;
  
  const [a, b] = parts;
  
  if (a === 127) return true; // Loopback
  if (a === 10) return true;  // Private
  if (a === 172 && b >= 16 && b <= 31) return true; // Private
  if (a === 192 && b === 168) return true; // Private
  if (a === 169 && b === 254) return true; // Link Local
  if (a === 0) return true;
  
  return false;
}

app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    activeBrowsers,
    queueLength: requestQueue.length,
    maxConcurrent: MAX_CONCURRENT_BROWSERS
  });
});

app.get('/screenshot', async (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Cache-Control', 'public, max-age=300');

  let targetUrl = req.query.url;
  if (!targetUrl) return res.status(400).send('Missing required "url" parameter.');

  if (!/^https?:\/\//i.test(targetUrl)) {
    targetUrl = 'https://' + targetUrl;
  }

  const safetyCheck = await validateUrlSafety(targetUrl);
  if (!safetyCheck.safe) {
    return res.status(403).send(`Security Error: ${safetyCheck.reason}`);
  }

  try {
    await acquireSlot(15000);
  } catch (err) {
    return res.status(503).send(err.message);
  }

  let browser = null;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--disable-software-rasterizer',
        '--no-zygote',
        '--disable-file-downloads',
        '--no-first-run',
        '--no-default-browser-check',
        '--mute-audio',
        '--disable-background-networking'
      ]
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800, deviceScaleFactor: 1 });

    // Request interception for speed optimization & security
    await page.setRequestInterception(true);
    page.on('request', (request) => {
      const reqUrl = request.url();
      const resourceType = request.resourceType();

      if (reqUrl.startsWith('file://') || reqUrl.startsWith('data:text/html')) {
        return request.abort();
      }

      // Block heavy media to dramatically boost screenshot render speeds
      if (['media', 'websocket', 'other'].includes(resourceType)) {
        return request.abort();
      }

      request.continue();
    });

    let navSuccess = false;
    let navUrl = safetyCheck.url;

    // Primary navigation attempt with timeout protection
    try {
      await page.goto(navUrl, {
        waitUntil: 'domcontentloaded',
        timeout: 15000
      });
      navSuccess = true;
    } catch (navErr) {
      console.warn(`Primary navigation warning for ${navUrl}: ${navErr.message}`);
      
      // Fallback: If HTTPS failed or timed out, attempt HTTP fallback if applicable
      if (navUrl.startsWith('https://')) {
        const httpUrl = navUrl.replace('https://', 'http://');
        try {
          await page.goto(httpUrl, { waitUntil: 'domcontentloaded', timeout: 12000 });
          navSuccess = true;
        } catch (httpErr) {
          console.warn(`HTTP fallback navigation failed for ${httpUrl}: ${httpErr.message}`);
        }
      }
    }

    // Small delay to allow CSS animations and image renders to settle
    await new Promise(r => setTimeout(r, 1200));

    // Capture screenshot even if networkidle wasn't completely reached (partial render fallback)
    const screenshot = await page.screenshot({
      fullPage: false,
      type: 'png'
    });

    res.set('Content-Type', 'image/png');
    return res.send(screenshot);

  } catch (error) {
    console.error(`Error taking screenshot for ${targetUrl}:`, error.message);
    return res.status(500).send('Screenshot capture error: ' + error.message);
  } finally {
    releaseSlot();
    if (browser) {
      try {
        await browser.close();
      } catch (e) {
        // Ignore browser close exception
      }
    }
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🔒 Robust Screenshot service running on port ${PORT}`));

