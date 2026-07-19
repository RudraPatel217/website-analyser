import ssl
import socket
import requests
import math
from datetime import datetime
from bs4 import BeautifulSoup
import urllib3

# Disable warning messages for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_ssl_details(hostname):
    """
    Validates the target SSL certificate and extracts details like issuer, expiration date, etc.
    """
    context = ssl.create_default_context()
    # Accept self-signed / expired certs for analysis
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        # Fetch certificate details using standard verification first
        context_strict = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=6) as sock:
            with context_strict.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                if cert:
                    expire_str = cert.get('notAfter')
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    common_name = issuer.get('commonName', 'N/A')
                    organization = issuer.get('organizationName', 'N/A')
                    
                    expire_date = datetime.strptime(expire_str, '%b %d %H:%M:%S %Y %Z')
                    days_left = (expire_date - datetime.utcnow()).days
                    
                    return {
                        "valid": True,
                        "issuer_cn": common_name,
                        "issuer_org": organization,
                        "expiry_date": expire_date.strftime("%Y-%m-%d"),
                        "days_left": max(0, days_left),
                        "error": ""
                    }
    except Exception as strict_error:
        # Retry without strict validation to check if certificate is present but untrusted/expired
        try:
            with socket.create_connection((hostname, 443), timeout=6) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert(binary_form=True)
                    # Cert exists but signature verification failed (e.g. self-signed or expired)
                    return {
                        "valid": False,
                        "issuer_cn": "Self-Signed or Untrusted",
                        "issuer_org": "N/A",
                        "expiry_date": "N/A",
                        "days_left": 0,
                        "error": f"Untrusted Certificate: {str(strict_error)}"
                    }
        except Exception as e:
            return {
                "valid": False,
                "issuer_cn": "N/A",
                "issuer_org": "N/A",
                "expiry_date": "N/A",
                "days_left": -1,
                "error": f"Connection/SSL Port 443 Closed: {str(e)}"
            }

def check_security_headers(url):
    """
    Checks HTTP response headers for missing key security configurations.
    """
    headers_to_check = {
        "Strict-Transport-Security": "HSTS ensures all connections are encrypted.",
        "Content-Security-Policy": "CSP prevents Cross-Site Scripting (XSS) and code injection.",
        "X-Frame-Options": "Prevents Clickjacking attacks by restricting framing.",
        "X-Content-Type-Options": "Prevents MIME-sniffing exploits by forcing declared content types.",
        "Referrer-Policy": "Restricts referrer info transmitted during navigation."
    }
    
    findings = []
    compliance_score = 100
    status_code = 0
    response_time = 0.0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        start_time = datetime.now()
        # Verify=False to allow checking headers on self-signed/expired cert websites
        resp = requests.get(url, timeout=8, headers=headers, allow_redirects=True, verify=False)
        response_time = (datetime.now() - start_time).total_seconds()
        status_code = resp.status_code
        resp_headers = resp.headers
        
        for header_name, desc in headers_to_check.items():
            value = resp_headers.get(header_name)
            if value:
                findings.append({
                    "header": header_name,
                    "status": "Present",
                    "value": value[:60] + "..." if len(value) > 60 else value,
                    "desc": desc,
                    "severity": "Info"
                })
            else:
                severity = "High" if header_name in ["Content-Security-Policy", "Strict-Transport-Security"] else "Medium"
                findings.append({
                    "header": header_name,
                    "status": "Missing",
                    "value": "N/A",
                    "desc": desc,
                    "severity": severity
                })
                # Deduct points based on missing headers
                compliance_score -= 20 if severity == "High" else 10
                
    except Exception as e:
        status_code = 500
        compliance_score = 0
        findings = [{"header": h, "status": "Error", "value": str(e), "desc": desc, "severity": "High"} for h, desc in headers_to_check.items()]
        
    return findings, max(0, compliance_score), status_code, round(response_time, 3)

def calculate_entropy(s):
    """
    Calculates the Shannon Entropy of a string to detect randomized domain names.
    """
    if not s:
        return 0.0
    entropy = 0.0
    for x in range(256):
        p_x = float(s.count(chr(x))) / len(s)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def check_phishing_heuristics(domain, whois_creation_str="N/A"):
    """
    Evaluates domain traits for brand spoofing, random generation, and age indicators.
    """
    risk_score = 0
    reasons = []
    
    # 1. Brand Spoofing / Typo-squatting
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
                reasons.append(f"Suspicious Brand Association: Domain contains brand keyword '{brand}' but does not match official endpoints.")
                
    # 2. String Entropy Checks
    entropy = calculate_entropy(domain.split(".")[0])
    if entropy > 4.2:
        risk_score += 25
        reasons.append(f"High String Entropy ({entropy:.2f}): Domain name structure displays random distribution patterns typical of algorithmic generation.")
        
    # 3. Nesting Level Checks
    subdomains = domain.split(".")
    if len(subdomains) > 4:
        risk_score += 15
        reasons.append(f"High Subdomain Nesting Level ({len(subdomains)}): Phishing URLs frequently nest multiple subdomains to spoof brand URLs.")
        
    # 4. Domain Age from WHOIS
    if whois_creation_str and whois_creation_str != "N/A":
        try:
            creation_date = datetime.strptime(whois_creation_str, "%Y-%m-%d")
            age_days = (datetime.now() - creation_date).days
            if age_days < 180:
                risk_score += 20
                reasons.append(f"Newly Registered Domain ({age_days} days old): High-risk indicator as phishing domains are short-lived.")
        except Exception:
            pass
            
    # 5. TLD Risk Profiling
    high_risk_tlds = [".xyz", ".top", ".cc", ".fit", ".gq", ".cf", ".tk", ".ml", ".ga", ".work"]
    for tld in high_risk_tlds:
        if clean_domain.endswith(tld):
            risk_score += 15
            reasons.append(f"High-Risk TLD: Domain registered under '{tld}' which experiences disproportionately high phishing traffic.")
            
    return min(100, risk_score), reasons

def check_malware_heuristics(html_content):
    """
    Scans HTML node architecture and script attributes for malicious indicators.
    """
    risk_score = 0
    reasons = []
    
    if not html_content:
        return 0, []
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Hidden frames
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
        reasons.append(f"Hidden Iframes ({hidden_iframes}): Invisible iframes detected on landing layout, commonly utilized for drive-by download exploits.")
        
    # 2. Code Obfuscation Markers
    scripts = soup.find_all('script')
    eval_calls = 0
    obfuscated_encoding = 0
    
    for s in scripts:
        if s.string:
            s_text = s.string
            if "eval(" in s_text or "eval(" in s_text.replace(" ", ""):
                eval_calls += 1
            if "unescape(" in s_text or "String.fromCharCode" in s_text:
                obfuscated_encoding += 1
                
    if eval_calls > 0:
        risk_score += 30
        reasons.append(f"Dynamic Script Execution: Found usage of dynamic execution wrapper 'eval()', widely used to execute obfuscated malicious payloads.")
    if obfuscated_encoding > 0:
        risk_score += 20
        reasons.append(f"Obfuscation Utility: Detected script encoding signatures ('unescape' or 'fromCharCode') that mask dynamic code payloads.")
        
    # 3. High Surface Script Resources
    external_scripts = 0
    for s in scripts:
        src = s.get('src', '')
        if src and (src.startswith('http://') or src.startswith('https://')):
            external_scripts += 1
            
    if external_scripts > 15:
        risk_score += 15
        reasons.append(f"Supply-Chain Vulnerability: Excess script nodes ({external_scripts}) loaded from outside domains, inflating client security exposure.")
        
    return min(100, risk_score), reasons

def run_cyber_scan(domain, original_url, html_content, whois_creation_str="N/A"):
    """
    Executes a complete cybersecurity analysis on the target.
    """
    ssl_info = get_ssl_details(domain)
    header_findings, header_score, status_code, load_time = check_security_headers(original_url)
    phish_score, phish_reasons = check_phishing_heuristics(domain, whois_creation_str)
    malware_score, malware_reasons = check_malware_heuristics(html_content)
    
    # Calculate global security compliance metric
    # Deductions:
    # - 30% weight to Phishing risk
    # - 30% weight to Malware risk
    # - 20% weight to missing Security Headers
    # - 20% weight to invalid SSL / closed SSL port
    ssl_deduction = 0 if ssl_info["valid"] else 20
    header_deduction = (100 - header_score) * 0.2
    phish_deduction = phish_score * 0.3
    malware_deduction = malware_score * 0.3
    
    global_score = round(100 - (ssl_deduction + header_deduction + phish_deduction + malware_deduction))
    global_score = max(0, min(100, global_score))
    
    # Map score to Security Grade
    if global_score >= 90:
        grade = "A"
        rating = "Low Risk"
    elif global_score >= 80:
        grade = "B"
        rating = "Low Risk"
    elif global_score >= 70:
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
    if not ssl_info["valid"]:
        recommendations.append("Secure Port 443 and provision a valid SSL certificate signed by a trusted Authority.")
    elif ssl_info["days_left"] < 30:
        recommendations.append(f"SSL certificate expires in {ssl_info['days_left']} days. Plan immediate renewal.")
        
    for finding in header_findings:
        if finding["status"] == "Missing":
            recommendations.append(f"Enable security header '{finding['header']}'. {finding['desc']}")
            
    if phish_score > 30:
        recommendations.append("Review domain registration details and enforce brand-protection/trademark legal notices.")
    if malware_score > 30:
        recommendations.append("Scan repository source files to remove obfuscated scripts and suspicious external dynamic links.")
        
    if not recommendations:
        recommendations.append("No active vulnerabilities found. Keep server configurations up to date.")
        
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
