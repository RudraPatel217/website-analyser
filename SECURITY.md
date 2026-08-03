# 🛡️ Security Policy & Hardening Guidelines

## Security Overview

The **Domain Intelligence Agent & SEO Auditor** is engineered with defense-in-depth security principles to protect both host environments and target websites during scanning.

---

## Implemented Security Safeguards

### 1. Server-Side Request Forgery (SSRF) Protection
- **Target Network Validation**: All user-entered domain inputs undergo real-time DNS resolution checks before any network request or Puppeteer preview is initialized.
- **Forbidden IP Ranges**: Requests targeting loopback addresses (`127.0.0.1`, `localhost`, `0.0.0.0`, `::1`), RFC 1918 private subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), and AWS/Cloud Instance Metadata Services (`169.254.169.254`) are strictly blocked.
- **Protocol Whitelisting**: Network connections are strictly limited to `http://` and `https://` schemes. Protocols such as `file://`, `gopher://`, and `ftp://` are rejected.

### 2. Microservice Hardening (`screenshot-service`)
- **Rate Limiting**: Integrated `express-rate-limit` middleware limits requests to 30 requests/minute per IP address to mitigate Denial-of-Service (DoS) vectors.
- **Resource Concurrency Locking**: Capped at maximum 3 concurrent headless Chromium browser processes to prevent server memory depletion.
- **Browser Sandboxing & Navigation Restrictions**: Request interception blocks `file://` navigations, local frame injection, and automatic file downloads.

### 3. Streamlit Security Policies
- **Cross-Site Request Forgery (XSRF)**: Enabled `enableXsrfProtection = true` in `.streamlit/config.toml`.
- **CORS Restrictions**: Configured `enableCORS = false` for strict origin control.
- **Telemetry Isolation**: Usage tracking disabled (`gatherUsageStats = false`).

### 4. API Key Protection & Visitor Overrides
- **Zero Exposure**: Admin API keys configured in environment variables or Streamlit Cloud Secrets are executed server-side and **never exposed** to visitor browsers, client JavaScript, DOM elements, or export logs.
- **In-App Password Masking**: Visitor API key inputs use password fields (`type="password"`) so keys are masked (`••••••••`) on screen.
- **Visitor Custom Keys**: App users can enter their own API keys in the **🔑 API Key Settings** expander. User-entered keys override server defaults for that session only and are never saved or persisted.
- **Public API Fallback**: If no API key is provided, the app seamlessly defaults to free public screenshot services (Microlink / WordPress mShot) requiring zero API keys.

---

## Safe Deployment Checklist for GitHub Users

When deploying this project publicly or to cloud providers (e.g., Streamlit Community Cloud, Render, Railway):

1. **Never commit `.env` to GitHub**:
   Use `.env.example` as a reference and set secret keys in your cloud provider's Environment Variables setting.
2. **Environment Secrets on Streamlit Cloud**:
   Add secrets under **Settings > Secrets**:
   ```toml
   GTMETRIX_API_KEY = "your_key_here"
   BUILTWITH_API_KEY = "your_key_here"
   ```
3. **User Instructions for Getting Their Own Keys**:
   - **GTmetrix API**: Sign up for a free key at [gtmetrix.com/api](https://gtmetrix.com/api/).
   - **BuiltWith API**: Sign up for a key at [builtwith.com/api](https://builtwith.com/api).

---

## Reporting Vulnerabilities

If you discover a potential security flaw in this project, please open a private GitHub issue or contact the maintainers directly.
