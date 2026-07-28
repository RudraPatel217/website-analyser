import ssl
import socket
import requests
import math
import re
from urllib.parse import urlparse
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import urllib3

# Disable warning messages for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def is_safe_public_domain(hostname):
    """
    Sanitizes target domains and prevents Server-Side Request Forgery (SSRF)
    by blocking requests targeting internal loopback or private IP ranges.
    """
    clean_host = hostname.lower().strip().replace("https://", "").replace("http://", "").split("/")[0].split(":")[0]
    
    # Block explicit localhost or metadata endpoints
    if clean_host in ["localhost", "127.0.0.1", "0.0.0.0", "::1", "169.254.169.254"]:
        return False, "Target resolves to local loopback or cloud metadata IP address (SSRF Protection Triggered)."
        
    try:
        ip_addr = socket.gethostbyname(clean_host)
        ip_parts = [int(p) for p in ip_addr.split('.')]
        
        # Check RFC1918 private subnets: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8
        if ip_parts[0] == 10:
            return False, f"Domain resolves to private IP range {ip_addr} (10.0.0.0/8)."
        if ip_parts[0] == 172 and 16 <= ip_parts[1] <= 31:
            return False, f"Domain resolves to private IP range {ip_addr} (172.16.0.0/12)."
        if ip_parts[0] == 192 and ip_parts[1] == 168:
            return False, f"Domain resolves to private IP range {ip_addr} (192.168.0.0/16)."
        if ip_parts[0] == 127:
            return False, f"Domain resolves to loopback IP range {ip_addr}."
    except Exception:
        pass

    return True, ""

def get_ssl_details(hostname):
    """
    Validates SSL/TLS certificate, checks protocol version (TLSv1.3/TLSv1.2), and expiration telemetry.
    """
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    tls_version = "Unknown"
    cipher_name = "N/A"
    
    try:
        # Strict validation attempt
        context_strict = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=6) as sock:
            with context_strict.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                tls_version = ssock.version() or "TLSv1.2+"
                c_info = ssock.cipher()
                cipher_name = c_info[0] if (c_info and len(c_info) > 0) else "N/A"
                
                if cert and isinstance(cert, dict):
                    expire_str = cert.get('notAfter')
                    common_name = "N/A"
                    organization = "N/A"
                    
                    issuer_tuple = cert.get('issuer', ())
                    if issuer_tuple:
                        for entry in issuer_tuple:
                            for item in entry:
                                if len(item) == 2:
                                    k, v = item
                                    if k == 'commonName':
                                        common_name = v if isinstance(v, str) else str(v)
                                    elif k == 'organizationName':
                                        organization = v if isinstance(v, str) else str(v)
                    
                    if isinstance(expire_str, str):
                        expire_date = datetime.strptime(expire_str, '%b %d %H:%M:%S %Y %Z')
                        days_left = (expire_date - datetime.now(timezone.utc).replace(tzinfo=None)).days
                        return {
                            "valid": True,
                            "issuer_cn": common_name,
                            "issuer_org": organization,
                            "expiry_date": expire_date.strftime("%Y-%m-%d"),
                            "days_left": max(0, days_left),
                            "tls_version": tls_version,
                            "cipher": cipher_name,
                            "error": ""
                        }
    except Exception as strict_error:
        # Fallback to inspect non-verified peer cert
        try:
            with socket.create_connection((hostname, 443), timeout=6) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    ssock.getpeercert(binary_form=True)
                    tls_version = ssock.version() or "Legacy TLS"
                    return {
                        "valid": False,
                        "issuer_cn": "Self-Signed or Untrusted",
                        "issuer_org": "N/A",
                        "expiry_date": "N/A",
                        "days_left": 0,
                        "tls_version": tls_version,
                        "cipher": cipher_name,
                        "error": f"Untrusted Certificate: {str(strict_error)}"
                    }
        except Exception as e:
            return {
                "valid": False,
                "issuer_cn": "N/A",
                "issuer_org": "N/A",
                "expiry_date": "N/A",
                "days_left": -1,
                "tls_version": "N/A",
                "cipher": "N/A",
                "error": f"Port 443 Unreachable: {str(e)}"
            }

    return {
        "valid": False,
        "issuer_cn": "N/A",
        "issuer_org": "N/A",
        "expiry_date": "N/A",
        "days_left": -1,
        "tls_version": tls_version,
        "cipher": cipher_name,
        "error": "Certificate telemetry unavailable"
    }

def check_security_headers(url):
    """
    Audits HTTP response headers against OWASP Security Headers guidelines.
    """
    headers_to_check = {
        "Strict-Transport-Security": "HSTS ensures encrypted HTTPS connections and mitigates downgrade attacks.",
        "Content-Security-Policy": "CSP prevents Cross-Site Scripting (XSS), clickjacking, and code injection.",
        "X-Frame-Options": "Prevents Clickjacking attacks by restricting page embedding in iframes.",
        "X-Content-Type-Options": "Disables MIME-sniffing exploits by forcing declared content types.",
        "Referrer-Policy": "Restricts sensitive referral data sent during cross-origin navigation.",
        "Permissions-Policy": "Restricts browser feature access (camera, microphone, geolocation).",
        "Cross-Origin-Opener-Policy": "COOP isolates top-level window context to mitigate Spectre attacks.",
        "X-XSS-Protection": "Legacy XSS filter header protecting older browser clients."
    }
    
    findings = []
    compliance_score = 100
    status_code = 0
    response_time = 0.0
    server_header = "N/A"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        start_time = datetime.now()
        resp = requests.get(url, timeout=8, headers=headers, allow_redirects=True, verify=False)
        response_time = (datetime.now() - start_time).total_seconds()
        status_code = resp.status_code
        resp_headers = resp.headers
        
        server_header = resp_headers.get("Server", resp_headers.get("X-Powered-By", "Hidden/N/A"))
        
        for header_name, desc in headers_to_check.items():
            value = resp_headers.get(header_name)
            if value:
                findings.append({
                    "header": header_name,
                    "status": "Present",
                    "value": value[:65] + "..." if len(value) > 65 else value,
                    "desc": desc,
                    "severity": "Info"
                })
            else:
                high_sev_headers = ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options"]
                severity = "High" if header_name in high_sev_headers else "Medium"
                findings.append({
                    "header": header_name,
                    "status": "Missing",
                    "value": "N/A",
                    "desc": desc,
                    "severity": severity
                })
                compliance_score -= 15 if severity == "High" else 8
                
    except Exception as e:
        status_code = 500
        compliance_score = 0
        findings = [{"header": h, "status": "Error", "value": str(e), "desc": desc, "severity": "High"} for h, desc in headers_to_check.items()]
        
    return findings, max(0, compliance_score), status_code, round(response_time, 3), server_header

def calculate_entropy(s):
    if not s:
        return 0.0
    entropy = 0.0
    for x in range(256):
        p_x = float(s.count(chr(x))) / len(s)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def check_phishing_heuristics(domain, whois_creation_str="N/A"):
    risk_score = 0
    reasons = []
    
    popular_brands = ["paypal", "google", "microsoft", "facebook", "netflix", "apple", "amazon", "instagram", "linkedin", "twitter", "bank", "secure", "login", "update", "verify"]
    clean_domain = domain.lower()
    
    for brand in popular_brands:
        if brand in clean_domain:
            legit_endings = [f"{brand}.com", f"{brand}.net", f"{brand}.org", f"{brand}.co"]
            is_legit = False
            for ending in legit_endings:
                if clean_domain == ending or clean_domain.endswith("." + ending):
                    is_legit = True
                    break
            if not is_legit:
                risk_score += 40
                reasons.append(f"Brand Impersonation Risk: Domain keyword '{brand}' does not match official domain endpoints.")
                
    entropy = calculate_entropy(domain.split(".")[0])
    if entropy > 4.2:
        risk_score += 25
        reasons.append(f"High Name Entropy ({entropy:.2f}): Algorithmic pattern typical of automated phishing domain generation.")
        
    subdomains = domain.split(".")
    if len(subdomains) > 4:
        risk_score += 15
        reasons.append(f"Excess Subdomain Depth ({len(subdomains)} levels): Used to obfuscate true origin domain.")
        
    if whois_creation_str and whois_creation_str != "N/A":
        try:
            creation_date = datetime.strptime(whois_creation_str, "%Y-%m-%d")
            age_days = (datetime.now() - creation_date).days
            if age_days < 180:
                risk_score += 20
                reasons.append(f"Newly Registered Domain ({age_days} days old): Higher risk tier for phishing and malware campaigns.")
        except Exception:
            pass
            
    high_risk_tlds = [".xyz", ".top", ".cc", ".fit", ".gq", ".cf", ".tk", ".ml", ".ga", ".work"]
    for tld in high_risk_tlds:
        if clean_domain.endswith(tld):
            risk_score += 15
            reasons.append(f"High-Risk TLD: Domain registered under top-level domain '{tld}' associated with high abuse rates.")
            
    return min(100, risk_score), reasons

def check_malware_and_code_vulnerabilities(html_content, is_https=True):
    """
    Scans HTML architecture for malware signatures, obfuscation, sensitive key leaks, and form vulnerabilities.
    """
    risk_score = 0
    reasons = []
    
    if not html_content:
        return 0, []
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Hidden Frames Inspection
    iframes = soup.find_all('iframe')
    hidden_iframes = 0
    for iframe in iframes:
        style = (iframe.get('style', '') or '').lower()
        width = (iframe.get('width', '') or '')
        height = (iframe.get('height', '') or '')
        if 'display:none' in style or 'visibility:hidden' in style or width == '0' or height == '0':
            hidden_iframes += 1
            
    if hidden_iframes > 0:
        risk_score += 35
        reasons.append(f"Hidden Iframes ({hidden_iframes} detected): Invisible frames commonly exploited for drive-by downloads.")
        
    # 2. Obfuscation & Dynamic Script Execution
    scripts = soup.find_all('script')
    eval_calls = 0
    obfuscated_encoding = 0
    
    for s in scripts:
        if s.string:
            s_text = s.string
            if "eval(" in s_text:
                eval_calls += 1
            if "unescape(" in s_text or "String.fromCharCode" in s_text:
                obfuscated_encoding += 1
                
    if eval_calls > 0:
        risk_score += 25
        reasons.append(f"Dynamic Execution ('eval'): Detected usage of `eval()` wrappers which mask dynamic script execution.")
    if obfuscated_encoding > 0:
        risk_score += 20
        reasons.append(f"Code Obfuscation Signatures: Script uses `unescape` or `fromCharCode` encoding patterns.")
        
    # 3. Secret Leakage Detection (API Keys, JWTs, AWS Creds)
    raw_html = str(html_content)
    secret_patterns = {
        "AWS Access Key": r'AKIA[0-9A-Z]{16}',
        "OpenAI / Secret API Key": r'sk-[a-zA-Z0-9_-]{32,}',
        "JWT Signature Token": r'eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}',
        "Private RSA Key Header": r'-----BEGIN PRIVATE KEY-----'
    }
    
    for secret_name, pattern in secret_patterns.items():
        if re.search(pattern, raw_html):
            risk_score += 40
            reasons.append(f"Exposed Secret Credential: Found pattern matching '{secret_name}' in public frontend source.")

    # 4. Form Security Audit (Insecure Submissions / Missing CSRF)
    forms = soup.find_all('form')
    for form in forms:
        action = (form.get('action', '') or '').lower()
        if action.startswith('http://') and is_https:
            risk_score += 25
            reasons.append("Insecure Form Action: HTTPS page submits form credentials to insecure `http://` URL.")
            break
            
    # 5. Mixed Content Check (HTTP assets on HTTPS site)
    if is_https:
        insecure_assets = 0
        for tag, attr in [('script', 'src'), ('link', 'href'), ('img', 'src')]:
            for elem in soup.find_all(tag):
                src_val = elem.get(attr, '')
                if src_val.startswith('http://'):
                    insecure_assets += 1
        if insecure_assets > 0:
            risk_score += 15
            reasons.append(f"Mixed Content Assets ({insecure_assets} HTTP resources): Scripts/images loaded over unencrypted HTTP.")

    return min(100, risk_score), reasons

def run_cyber_scan(domain, original_url, html_content, whois_creation_str="N/A"):
    """
    Runs an enterprise cybersecurity audit on target domain.
    """
    # SSRF Protection Check
    is_safe, ssrf_msg = is_safe_public_domain(domain)
    if not is_safe:
        return {
            "domain": domain,
            "url": original_url,
            "global_score": 0,
            "grade": "F",
            "rating": "Critical Risk (SSRF)",
            "ssl_info": {"valid": False, "issuer_cn": "N/A", "issuer_org": "N/A", "expiry_date": "N/A", "days_left": 0, "tls_version": "N/A", "cipher": "N/A", "error": ssrf_msg},
            "headers_score": 0,
            "header_findings": [],
            "phishing_score": 100,
            "phishing_reasons": [ssrf_msg],
            "malware_score": 0,
            "malware_reasons": [],
            "status_code": 403,
            "load_time": 0.0,
            "recommendations": ["Do not scan internal, private, or loopback network targets."],
            "timestamp": datetime.now().isoformat()
        }

    is_https = original_url.startswith("https://")
    ssl_info = get_ssl_details(domain)
    header_findings, header_score, status_code, load_time, server_header = check_security_headers(original_url)
    phish_score, phish_reasons = check_phishing_heuristics(domain, whois_creation_str)
    malware_score, malware_reasons = check_malware_and_code_vulnerabilities(html_content, is_https)
    
    # Calculate global security compliance metric
    ssl_is_valid = bool(ssl_info.get("valid", False))
    ssl_deduction = 0 if ssl_is_valid else 25
    header_deduction = (100 - header_score) * 0.25
    phish_deduction = phish_score * 0.25
    malware_deduction = malware_score * 0.25
    
    global_score = round(100 - (ssl_deduction + header_deduction + phish_deduction + malware_deduction))
    global_score = max(0, min(100, global_score))
    
    # Map score to Security Grade
    if global_score >= 95:
        grade = "A+"
        rating = "Optimal Security"
    elif global_score >= 88:
        grade = "A"
        rating = "Low Risk"
    elif global_score >= 78:
        grade = "B"
        rating = "Low Risk"
    elif global_score >= 68:
        grade = "C"
        rating = "Medium Risk"
    elif global_score >= 50:
        grade = "D"
        rating = "High Risk"
    else:
        grade = "F"
        rating = "Critical Risk"
        
    # Generate actionable remediation checklist
    recommendations = []
    days_left_val = ssl_info.get("days_left", -1)
    
    if not ssl_is_valid:
        recommendations.append("Secure Port 443 and provision a valid SSL/TLS certificate from a trusted Authority.")
    elif isinstance(days_left_val, int) and 0 <= days_left_val < 30:
        recommendations.append(f"SSL certificate expires in {days_left_val} days. Plan immediate renewal.")
        
    for finding in header_findings:
        if finding["status"] == "Missing":
            recommendations.append(f"Enable security header '{finding['header']}'. {finding['desc']}")
            
    if server_header != "N/A" and ("Apache/" in server_header or "nginx/" in server_header or "PHP/" in server_header):
        recommendations.append(f"Suppress backend server version tokens in HTTP headers (Currently exposing: '{server_header}').")
        
    if phish_score > 30:
        recommendations.append("Review domain registration details and enforce brand-protection/trademark legal notices.")
    if malware_score > 30:
        recommendations.append("Scan repository source files to remove obfuscated scripts and suspicious external dynamic links.")
        
    if not recommendations:
        recommendations.append("No active vulnerabilities found. Keep server software and TLS configurations up to date.")
        
    return {
        "domain": domain,
        "url": original_url,
        "global_score": global_score,
        "grade": grade,
        "rating": rating,
        "ssl_info": ssl_info,
        "headers_score": header_score,
        "header_findings": header_findings,
        "phishing_score": phish_score,
        "phishing_reasons": phish_reasons,
        "malware_score": malware_score,
        "malware_reasons": malware_reasons,
        "status_code": status_code,
        "load_time": load_time,
        "recommendations": recommendations,
        "timestamp": datetime.now().isoformat()
    }
