# 🛡️ Contribution & Repository Security Guidelines

Thank you for your interest in contributing to the **Domain Intelligence Agent & SEO Auditor**!

To ensure the safety, security, and integrity of this open-source project, strict contribution rules are enforced.

---

## 🔒 Security & Push Controls

1. **Direct Pushes Restricted**: Direct pushes to `main` or protected feature branches are disabled. All changes must be submitted via **Pull Requests (PRs)**.
2. **Code Owner Approval Required**: Every Pull Request requires explicit review and approval from the repository maintainer (`@RudraPatel217`) before merging.
3. **Automated CI Security Checks**: All PRs automatically trigger GitHub Actions security workflows. PRs with failing security tests, secret leaks, or vulnerabilities will be automatically blocked.

---

## 🚀 How to Submit a Safe Contribution

1. **Fork the Repository**: Create your own fork on GitHub.
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Follow Security Hardening Guidelines**:
   - Never commit `.env` files or hardcoded API keys.
   - Do not weaken SSRF (Server-Side Request Forgery) IP validation in `agent/backend/cyber_scanner.py` or `agent/app.py`.
   - Ensure all Puppeteer sandbox configurations remain intact in `screenshot-service/server.js`.
4. **Run Verification**: Test Python compilation and Node.js security:
   ```bash
   python -m py_compile agent/app.py
   cd screenshot-service && npm audit
   ```
5. **Open a Pull Request**: Submit your PR targeting `main`. Describe your changes clearly and link any relevant issues.

---

## 🛡️ Security Vulnerability Reporting

If you identify a security vulnerability, please **do not open a public issue**. Follow the instructions in [SECURITY.md](SECURITY.md) to report it privately.
