# 🌐 Domain Intelligence Agent & SEO Auditor

[![Live Application](https://img.shields.io/badge/Live_App-website--analyser.streamlit.app-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://website-analyser.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Puppeteer](https://img.shields.io/badge/Puppeteer-40B5A4?style=for-the-badge&logo=Puppeteer&logoColor=white)](https://pptr.dev/)
[![Security: SSRF Protected](https://img.shields.io/badge/Security-SSRF%20Protected-brightgreen.svg?style=for-the-badge)](SECURITY.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An enterprise-grade, multi-website SEO Auditor and Domain Intelligence Tool. This application combines a fast Python-based crawler with multi-tiered cloud screenshot engines and cybersecurity protections, rendering an interactive, glassmorphic Streamlit dashboard for real-time diagnostics and comprehensive Excel reporting.

---

## 🔗 Official Live Application & Demo

You can use the fully deployed web application directly in your browser without any manual setup

---

## 🚀 Key Features

*   **Multi-Domain Crawling:** Audit single or multiple target domains simultaneously (default domain: `https://jeenweb.com`).
*   **Deep SEO Crawler:** Evaluates on-page SEO factors (Titles, Metas, H1, Canonical tags, OpenGraph tags, JSON-LD Schema structure) and calculates internal/external link profiles.
*   **Domain Intelligence Analytics:** Automatically resolves WHOIS data, nameservers, registrar creation/expiration dates, DNS MX records, and verifies SSL status.
*   **Multi-Tiered Screenshot Engine:** Flexible website visual previews supporting **Microlink Cloud API** (zero-config cloud default), **WordPress mShot API**, **Thum.io**, **GTmetrix API v2.0**, and **Local Puppeteer Service**.
*   **Cybersecurity & Risk Scorecard:** Evaluates 4 core security pillars (SSL/TLS validation, 6 HTTP Security Headers, Brand & Phishing protection, Malware HTML heuristics) with transparent scoring calculations.
*   **Enterprise Security & SSRF Protection:** Real-time DNS inspection blocking requests targeting loopback (`127.0.0.1`), private networks (`10.x`, `172.16-31.x`, `192.168.x`), and cloud metadata (`169.254.169.254`).
*   **Glassmorphic UI Theme:** Styled with custom Google Fonts (`Plus Jakarta Sans`), radial gradients, modern metric cards, and responsive hover effects.
*   **Multi-Sheet Excel Exporter:** Download consolidated Excel workbooks containing domain analytics, crawled pages, technical metrics, security audits, and structured recommendations.

---

## 🎨 Premium UI Aesthetics

The application overrides default Streamlit components with a custom, tailored CSS interface:
*   **Typography:** The layout uses the premium `Plus Jakarta Sans` Google Font.
*   **Glassmorphic Panels:** Cards feature blurred backdrops (`backdrop-filter: blur(16px)`), subtle borders, and deep shadows for a high-end feel.
*   **Live Scanning Loader:** When a crawl begins, a custom radial loader and log-stream component render the agent's real-time action telemetry.
*   **Responsive Previews:** Displayed website screenshots are rendered inside mock desktop browser frames.

---

## 📷 Flexible Screenshot Solutions

The agent provides 5 multi-tiered screenshot engines for maximum reliability:

| Screenshot Source | Works on Cloud Deployments? | Requires Local Setup? | Best Used For |
| :--- | :---: | :---: | :--- |
| **Microlink Cloud API** | ✅ Yes | ❌ No | **Default Cloud Engine** (Streamlit Cloud, Render, Railway). Zero setup required! |
| **WordPress mShot API** | ✅ Yes | ❌ No | Fast, lightweight public preview fallback. |
| **Thum.io API** | ✅ Yes | ❌ No | Fast secondary public fallback option. |
| **GTmetrix API v2.0** | ✅ Yes | ❌ No | Premium authorized speed & layout audit preview. |
| **Local Puppeteer Service** | ❌ Local/Docker Only | ✅ Yes | High-precision full desktop renders on local machine. |

> [!TIP]
> **Automatic Cloud Fallback:** If *Local Puppeteer Service* is selected on a cloud platform (where local Node.js is not running), the application automatically falls back to **Microlink Cloud API** so website previews always render without errors!

---

## 🛡️ Security Hardening

This project is hardened against common security threats:
*   **SSRF Shielding:** Prevents users from scanning internal servers or cloud metadata.
*   **Express Rate Limiting:** Capped at rate limits in `server.js` (with local loopback bypass).
*   **Browser Sandboxing:** Puppeteer isolates page execution, blocking `file://` scheme navigations and automated file downloads.
*   **Streamlit Protection:** XSRF protection enabled and telemetry disabled in `.streamlit/config.toml`.

For complete details, see [SECURITY.md](SECURITY.md).

---

## 📂 Project Structure

```
├── .gitignore                  # Git exclude rule list
├── Dockerfile                  # Production Docker container definition
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies list
├── SECURITY.md                 # Security safeguards and guidelines
├── agent/                      # Core Streamlit app directory
│   ├── app.py                  # Streamlit frontend entrypoint & main application
│   ├── config.py               # Configuration module
│   ├── .streamlit/             # Streamlit theme & security configuration
│   │   └── config.toml         # Custom dark theme & XSRF security settings
│   ├── backend/                # Scraper, WHOIS, DNS, and Excel helper scripts
│   │   ├── crawler.py          # BFS web crawler & SEO validation
│   │   ├── cyber_scanner.py    # SSL, Security headers, and SSRF domain validator
│   │   ├── gtmetrix.py         # GTmetrix API runner
│   │   ├── report_generator.py # Excel sheet compiler (openpyxl)
│   │   ├── seo_analyzer.py     # Fallback analyses and dataset generator
│   │   └── whois_dns.py        # WHOIS registrar lookup & DNS query handler
│   └── frontend/               # Custom UI stylesheet injects & components
│       ├── components.py       # Render methods for metrics, previews, loaders
│       └── styles.py           # Premium glassmorphic global styling
└── screenshot-service/         # Express + Puppeteer screenshot microservice
    ├── package.json            # Node.js dependencies
    └── server.js               # Rate-limited & SSRF-protected Puppeteer server
```

---

## 📊 Exported Report Details

The generated download `.xlsx` report contains five specialized tabs:
1.  **Domain_Info:** Domain Registrar details, expiry status, MX Records, Robots/Sitemap discovery.
2.  **Crawled_Pages:** Listing of all explored pages with Titles, Meta descriptions, H1 headers, and HTTP status codes.
3.  **SEO_Issues:** Full log of detected warnings/critical bugs with severity and recommended fixes.
4.  **Cybersecurity_Audit:** SSL certificate details, HTTP Security Headers compliance, and vulnerability score.
5.  **Technical_Audit:** Extended metrics including page load time (s), page size (KB), missing image alt tag counts, and Core Web Vitals.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

