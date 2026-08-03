const express = require('express');
const puppeteer = require('puppeteer');
const rateLimit = require('express-rate-limit');
const dns = require('dns').promises;
const { URL } = require('url');

const app = express();

// Security: Enforce rate limiting to prevent DoS attacks on screenshot generator
const limiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute window
  max: 30, // Limit each IP to 30 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many screenshot requests from this IP, please try again after a minute.' }
});

app.use('/screenshot', limiter);

// Concurrency Control: Max 3 concurrent Puppeteer browsers to prevent RAM depletion
let activeBrowsers = 0;
const MAX_CONCURRENT_BROWSERS = 3;

/**
 * SSRF Validator: Ensures requested target is a public domain/IP.
 * Blocks requests targeting loopback addresses, local network IPs, and cloud metadata endpoints.
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
 * Helper to test if an IPv4 address falls into RFC 1918 or loopback ranges
 */
function isPrivateIp(ip) {
  if (!ip || typeof ip !== 'string') return true;
  
  // IPv6 Loopback / Local
  if (ip === '::1' || ip.startsWith('fe80:') || ip.startsWith('fc00:')) return true;
  
  const parts = ip.split('.').map(Number);
  if (parts.length !== 4 || parts.some(isNaN)) return false;
  
  const [a, b] = parts;
  
  // 127.0.0.0/8 (Loopback)
  if (a === 127) return true;
  // 10.0.0.0/8 (Private)
  if (a === 10) return true;
  // 172.16.0.0/12 (Private)
  if (a === 172 && b >= 16 && b <= 31) return true;
  // 192.168.0.0/16 (Private)
  if (a === 192 && b === 168) return true;
  // 169.254.0.0/16 (Link Local / Cloud Metadata)
  if (a === 169 && b === 254) return true;
  // 0.0.0.0/8
  if (a === 0) return true;
  
  return false;
}

app.get('/health', (req, res) => {
  res.json({ status: 'OK', activeBrowsers, maxConcurrent: MAX_CONCURRENT_BROWSERS });
});

app.get('/screenshot', async (req, res) => {
  let targetUrl = req.query.url;
  if (!targetUrl) return res.status(400).send('Missing required "url" parameter.');

  // Prepend protocol if missing
  if (!/^https?:\/\//i.test(targetUrl)) {
    targetUrl = 'https://' + targetUrl;
  }

  // Perform Security & SSRF Validation
  const safetyCheck = await validateUrlSafety(targetUrl);
  if (!safetyCheck.safe) {
    return res.status(403).send(`Security Error: ${safetyCheck.reason}`);
  }

  // Concurrency Guard
  if (activeBrowsers >= MAX_CONCURRENT_BROWSERS) {
    return res.status(530).send('Screenshot service busy. Maximum concurrent browsers reached. Try again in a few seconds.');
  }

  activeBrowsers++;
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-file-downloads',
        '--no-first-run',
        '--no-default-browser-check'
      ]
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    // Block dangerous navigations / requests inside Puppeteer
    await page.setRequestInterception(true);
    page.on('request', (req) => {
      const reqUrl = req.url();
      if (reqUrl.startsWith('file://') || reqUrl.startsWith('data:text/html')) {
        req.abort();
      } else {
        req.continue();
      }
    });

    // Set viewport and goto with strict timeout
    await page.goto(safetyCheck.url, {
      waitUntil: 'networkidle2',
      timeout: 25000
    });

    const screenshot = await page.screenshot({
      fullPage: false, // Desktop viewport render for optimal performance
      type: 'png'
    });

    res.set('Content-Type', 'image/png');
    res.send(screenshot);

  } catch (error) {
    console.error(`Error taking screenshot for ${targetUrl}:`, error.message);
    res.status(500).send('Screenshot capture error: ' + error.message);
  } finally {
    activeBrowsers = Math.max(0, activeBrowsers - 1);
    if (browser) {
      try {
        await browser.close();
      } catch (e) {
        // Ignore close error
      }
    }
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🔒 Secure Screenshot service running on port ${PORT}`));
