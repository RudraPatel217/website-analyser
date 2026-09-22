# Domain Intelligence Agent & SEO Auditor

[![Live Application](https://img.shields.io/badge/Live_App-website--analyser.streamlit.app-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://website-analyser.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Puppeteer](https://img.shields.io/badge/Puppeteer-40B5A4?style=flat-square&logo=Puppeteer&logoColor=white)](https://pptr.dev/)
[![Security: SSRF Protected](https://img.shields.io/badge/Security-SSRF%20Protected-brightgreen.svg?style=flat-square)](SECURITY.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)

An end-to-end website audit and domain intelligence platform. The application combines a Python-based crawler, WHOIS and DNS query engines, cybersecurity risk diagnostics, multi-engine visual preview generation, and an interactive Streamlit frontend with comprehensive Excel report export.

Developed by [RudraPatel217](https://github.com/RudraPatel217).

---

## Live Application

The hosted version of this application is available online at:
https://website-analyser-rudra.streamlit.app

You can test single or multi-domain audits directly in the browser without installing local dependencies.

---

## Architecture Overview

The system consists of two core components:

1. **Frontend & Agent Core (Python / Streamlit):**
   - Interactive user interface with dark and light themes.
   - Multi-domain asynchronous crawler and SEO analyzer.
   - WHOIS registrar lookup, DNS MX record resolution, and SSL inspection.
   - Cybersecurity scorecard evaluating security headers and suspicious patterns.
   - Report generator producing structured multi-tab Excel files.

2. **Backend Screenshot & Render Microservice (Node.js / Express / Puppeteer):**
   - Headless browser service listening on port 3000 (`/screenshot` and `/render` endpoints).
   - Renders pixel-accurate desktop screenshots of target websites.
   - Executes headless Chrome with anti-detection flags (`--disable-blink-features=AutomationControlled`) to solve WAF/bot challenges (such as Cloudflare on LeetCode) and return fully rendered page HTML, titles, and metadata to the crawler.
   - Hardened with Server-Side Request Forgery (SSRF) verification, concurrency queues, and IP rate limiting.

---

## System Requirements

Before running the application locally, ensure your computer has the following tools installed:

- **Git:** For repository cloning.
- **Python 3.10 or higher** (Python 3.13 supported): For the frontend dashboard and crawling engine.
- **Node.js (v18 or higher recommended) and npm:** For the local Puppeteer backend screenshot service.
- **Google Chrome or Microsoft Edge** (Optional): Puppeteer will automatically detect system browsers or download Chromium.

---

## Local Setup and Installation

Follow these step-by-step instructions to set up the project on your local machine.

### Step 1: Clone the Repository

Open your terminal or command prompt and clone the repository:

```bash
git clone https://github.com/RudraPatel217/website-analyser.git
cd website-analyser
```

### Step 2: Set Up Python Virtual Environment (Frontend / Core)

Create and activate a virtual environment to isolate project dependencies:

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**On macOS and Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Upgrade pip and install the required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Set Up the Backend Screenshot Service

Navigate into the screenshot service directory and install its npm dependencies:

```bash
cd screenshot-service
npm install
cd ..
```

### Step 4: Environment Configuration (Optional)

The application works out of the box with zero external configuration. If you wish to use optional third-party integrations (such as GTmetrix API or BuiltWith API), create a `.env` file in the root folder:

```env
GTMETRIX_API_KEY=your_gtmetrix_api_key_here
BUILTWITH_API_KEY=your_builtwith_api_key_here
RATE_LIMIT_DELAY=2
```

---

## Running the Services

You can start the frontend and backend services either separately in two terminal windows or together using startup scripts.

### Method 1: Start Services Manually (Recommended for Development)

#### 1. Start the Backend Screenshot & Render Service (Port 3000)

In your first terminal, start the Node.js Express server:

```bash
cd screenshot-service
npm start
```

You should see:
```
🔒 Robust Screenshot service running on port 3000
Health check endpoint: http://localhost:3000/health
Screenshot endpoint:   http://localhost:3000/screenshot?url=https://example.com
Page render endpoint:  http://localhost:3000/render?url=https://example.com
```

#### 2. Start the Frontend Streamlit Application (Port 8501)

In a second terminal, activate your virtual environment from the project root and start Streamlit:

**On Windows:**
```cmd
venv\Scripts\activate
streamlit run app.py
```

**On macOS / Linux:**
```bash
source venv/bin/activate
streamlit run app.py
```

Streamlit will print the local URL:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in your browser to view the application.

---

### Method 2: One-Click Startup Scripts

Automated unified scripts are included in the root directory that automatically start both the Node.js Puppeteer service (port 3000) and the Streamlit application together:

- **Windows:** Double-click or run `start.bat`:
  ```cmd
  start.bat
  ```
  *Launches the Puppeteer background service on port 3000, then starts the Streamlit dashboard.*
- **macOS / Linux:** Run the shell script:
  ```bash
  chmod +x start.sh
  ./start.sh
  ```
  *Launches the Puppeteer background service on port 3000, runs the Streamlit app, and gracefully stops background processes on exit.*

---

### Method 3: Run with Docker Compose

If you have Docker and Docker Compose installed:

```bash
docker compose up --build
```

The application will be accessible at `http://localhost:8501`.

---

## How to Use the Application

1. Open the dashboard in your web browser (`http://localhost:8501`).
2. In the **Website Audit Setup** box, enter the target websites you want to inspect inside the text area (one URL per line). The input field displays `https://websitename.com` as a placeholder example.
3. Configure your audit parameters:
   - **Website Visual Preview Engine:** Choose between Instant Domain Snapshot, Ultra-Fast Visual Capture, or Local Puppeteer Engine (Port 3000).
   - **Max pages to scan per domain:** Adjust slider from 5 to 300 pages (default: 25).
   - **Scan Speed:** Select Accelerated Simulation (~5 min/website) or Thorough Deep Scan (~10 min/website).
4. Click **Start Full Multi-Website Analysis**.
5. Inspect live crawl telemetry, page audits, security scores, and domain records in the interactive tabs.
6. Click **Download Full Multi-Website Intelligence Report (.xlsx)** to save the complete workbook.

---

## Key Features

- **Multi-Domain Auditing:** Audit single or multiple domains concurrently.
- **Deep Technical SEO Inspection:** Crawls internal links, extracts page titles, meta descriptions, H1 headings, canonical URLs, OpenGraph metadata, and structured JSON-LD schemas.
- **Intelligent Bot Protection & WAF Resolution:** Accurately detects Cloudflare, Akamai, and WAF firewall challenges (HTTP 403/429/503). Automatically delegates to the local headless Chrome rendering engine to solve Turnstile challenges and extract genuine page metadata.
- **Zero False-Positive SEO Errors:** Guarantees that On-Page SEO tag audits (Title length, Meta Description length, H1 tags, Alt images) are only evaluated on authentic `200 OK` page content, completely preventing false warnings generated on anti-bot challenge or 4xx/5xx error pages.
- **In-Short Diagnostic Explanations:** Issues and errors in the dashboard explicitly state in short why they are displayed (e.g. `Bot Protection (403)`: *"Displayed because website has bot protection that blocks automated scanners; no further page information is given"*).
- **AI Recommendation Engine:** Heuristic reasoning engine that dynamically prioritizes remediation steps, including instructions to whitelist search engine bots (Googlebot, Bingbot) in Cloudflare/WAF firewall rules.
- **Domain Intelligence & DNS:** Queries WHOIS registrar info, domain creation/expiration dates, nameservers, DNS MX mail records, and SSL certificate validity.
- **Multi-Tier Visual Previews:**
  - Local Puppeteer engine running on port 3000 for local high-fidelity snapshots.
  - Ultra-Fast Visual Capture and cloud screenshot fallbacks for zero-setup cloud environments.
- **Cybersecurity & Heuristic Risk Scoring:** Audits SSL/TLS configuration, HTTP security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy), brand spoofing, and HTML heuristics.
- **SSRF Hardening:** Protects scanning endpoints by blocking requests to private networks, loopback addresses (`127.0.0.1`, `localhost`), and cloud metadata services (`169.254.169.254`).
- **Consolidated Excel Reports:** Generates five structured worksheets for Domain Info, Crawled Pages, SEO Issues, Cybersecurity Audit, and Technical Audit.

---

## Visual Preview Engine Comparison

| Engine | Local Machine | Cloud Deployments | Description |
| :--- | :--- | :--- | :--- |
| **Instant Domain Snapshot** | Supported | Supported | Zero-latency lightweight preview. |
| **Ultra-Fast Visual Capture** | Supported | Supported | Fast public snapshot waterfall for cloud hosting. |
| **Local Puppeteer Service** | Supported | Requires Node.js | Pixel-accurate local headless Chrome render on port 3000. |

---

## Project Structure

```
├── .gitignore                  # Git ignore file
├── Dockerfile                  # Container build instructions
├── docker-compose.yml          # Docker Compose service definition
├── requirements.txt            # Python dependencies
├── SECURITY.md                 # Security policies and SSRF documentation
├── start.bat                   # Windows one-click startup script (Streamlit + Puppeteer)
├── start.sh                    # Linux/macOS unified startup script
├── app.py                      # Root entrypoint redirecting to agent
├── agent/                      # Main application package
│   ├── app.py                  # Streamlit dashboard interface and audit flow
│   ├── config.py               # Secret and environment variable loader
│   ├── backend/                # Scraper, DNS, security, and report modules
│   │   ├── ai_recommendations.py# Heuristic SEO recommendation engine
│   │   ├── crawler.py          # BFS multi-page crawler with WAF detection & render fallback
│   │   ├── cyber_scanner.py    # SSL, HTTP headers, and SSRF validator
│   │   ├── gtmetrix.py         # GTmetrix API runner
│   │   ├── puppeteer_manager.py# Local Node.js service health and process manager
│   │   ├── report_generator.py # Excel workbook generator (openpyxl)
│   │   ├── seo_analyzer.py     # SEO metrics and issue detection
│   │   └── whois_dns.py        # WHOIS registrar and DNS MX resolution
│   └── frontend/               # UI components and custom styles
│       ├── components.py       # Metrics, loaders, and preview containers
│       └── styles.py           # Custom CSS and themes
└── screenshot-service/         # Express + Puppeteer microservice (Port 3000)
    ├── package.json            # Node.js dependencies
    └── server.js               # Rate-limited screenshot & /render server
```

---

## Excel Report Breakdown

The downloaded `.xlsx` report contains five sheets:

1. **Domain_Info:** Domain registration dates, registrar, DNS MX records, robots.txt, and sitemap detection.
2. **Crawled_Pages:** Comprehensive list of URLs scanned with HTTP status codes, titles, meta tags, and H1 elements.
3. **SEO_Issues:** Prioritized warnings and critical errors with specific recommendations for remediation.
4. **Cybersecurity_Audit:** SSL validity, missing security headers, phishing heuristics, and weighted risk scores.
5. **Technical_Audit:** Page load duration, missing image alt attributes, page sizes, and link profile counts.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
