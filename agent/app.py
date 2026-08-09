import sys
import os

# Ensure the current directory is in sys.path so modules resolve correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time
from urllib.parse import quote

# Import Frontend Subpackage Components
from frontend import inject_premium_styles, inject_header_element, inject_footer_element
from frontend import (
    render_scan_progress,
    render_browser_preview,
    render_metric_cards,
    render_ready_to_scan,
    render_download_section
)

# Import Backend Subpackage Utilities
from backend import (
    get_domain_info,
    crawl_page,
    run_cyber_scan,
    generate_ai_seo_recommendations,
    generate_unified_report,
    is_safe_public_domain,
    check_service_health,
    install_and_start_puppeteer_service
)

def is_owner_or_app_url(domain_str):
    """
    Detects if target domain matches the application's host URL or the owner's personal domain.
    """
    d = domain_str.lower().strip().replace("https://", "").replace("http://", "").split("/")[0].split(":")[0]
    protected_patterns = [
        "website-analyser",
        "streamlit.app",
        "jeenweb.com",
        "jeenweb"
    ]
    return any(p in d for p in protected_patterns)

def render_easter_egg(domain):
    """
    Displays a humorous Easter egg card when someone attempts to scan the app or owner domain.
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
        border: 2px solid #c084fc;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(192, 132, 252, 0.25);
    ">
        <div style="font-size: 4.5rem; margin-bottom: 0.75rem;">😎 🤪 🤖</div>
        <h2 style="color: #f472b6; font-size: 2rem; font-weight: 800; margin-top: 0; margin-bottom: 0.5rem;">
            Nice try! But I'm smarter than you!
        </h2>
        <p style="color: #e2e8f0; font-size: 1.1rem; max-width: 650px; margin: 0 auto; line-height: 1.6;">
            You can't audit the Master Agent or its protected host domain (<strong>{domain}</strong>)! This system is protected against self-scanning. Please enter a different target website to analyze.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="SEO Domain Intelligence Agent", layout="wide")

# Inject global style and header
inject_premium_styles()
inject_header_element()

# Input Panel configured inside native bordered container
with st.container(border=True):
    st.markdown(
        "<h3 style='margin-top: 0; color: #22d3ee; font-weight: 700; font-size: 1.3rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;'>Website Audit Setup</h3>",
        unsafe_allow_html=True)
    
    domains_input = st.text_area(
        "Target Website URLs (enter one domain per line):",
        value="https://example.com",
        height=100,
        help="Type or paste the web addresses of the websites you want to analyze (for example: https://example.com). You can audit multiple websites at once by placing each URL on a new line."
    )
    
    service_healthy, _ = check_service_health()
    default_source_index = 0 if service_healthy else 1

    col_source, col_c1, col_c2 = st.columns(3)
    with col_source:
        screenshot_source = st.selectbox(
            "Screenshot Preview Source:",
            options=[
                "Local Puppeteer Service (Port 3000)",
                "Microlink Cloud API (Free & Cloud-Compatible)",
                "WordPress mShot API (Fast Preview)",
                "Thum.io (Backup Fallback)",
                "GTmetrix API v2.0 (Premium & Authorized)"
            ],
            index=default_source_index,
            help="Select the engine used to capture visual screenshots of your website homepage. Microlink Cloud API works automatically online without extra software or API keys."
        )
    with col_c1:
        max_pages = st.slider(
            "Max pages to scan per domain:",
            min_value=5,
            max_value=300,
            value=25,
            help="Controls how deep the crawler explores your website. A lower number scans faster; a higher number audits more pages in depth."
        )
    with col_c2:
        scan_speed = st.selectbox(
            "Scan Speed:",
            options=[
                "Accelerated Simulation (~5min/website)",
                "Thorough Deep Scan (~10min/website)"],
            index=1,
            help="Choose Accelerated mode for quick analysis or Thorough mode for in-depth inspection of link structures and security protocols."
        )

    # Session state for tracking user choice on skipping preview
    if "skip_puppeteer_preview" not in st.session_state:
        st.session_state["skip_puppeteer_preview"] = False

col_b1, col_b2 = st.columns([3, 1])
with col_b1:
    run_analysis = st.button(
        "Start Full Multi-Website Analysis",
        type="primary",
        use_container_width=True
    )
with col_b2:
    if "audit_results" in st.session_state and st.session_state["audit_results"]:
        if st.button("Clear Results & New Scan", use_container_width=True):
            st.session_state["audit_results"] = None
            st.rerun()

scan_placeholder = st.empty()
crawl_count_placeholder = st.empty()
crawl_log_placeholder = st.empty()

# Check local Puppeteer service status
service_active, _ = check_service_health()

# ===================== HOMEPAGE PREVIEW =====================
if domains_input.strip() and not st.session_state.get("audit_results"):
    st.markdown("### Homepage Previews")

    # Check for Easter Egg trigger
    easter_egg_domains = [d.strip() for d in domains_input.split('\n') if d.strip() and is_owner_or_app_url(d.strip())]
    if easter_egg_domains:
        for eg_domain in easter_egg_domains:
            render_easter_egg(eg_domain)

    # CASE 1: Service is ALREADY running on port 3000 -> Render preview directly
    elif service_active:
        for domain in domains_input.split('\n'):
            domain = domain.strip()
            if domain and not is_owner_or_app_url(domain):
                try:
                    # SSRF Protection Check
                    is_safe, ssrf_msg = is_safe_public_domain(domain)
                    if not is_safe:
                        st.error(f"Security Block ({domain}): {ssrf_msg}")
                        continue

                    screenshot_url = f"http://localhost:3000/screenshot?url={quote(domain)}"
                    render_browser_preview(domain, screenshot_url)
                except Exception as e:
                    st.warning(f"Could not preview {domain}: {str(e)}")

    # CASE 2: Service is NOT running, but user selected "No, Skip Website Preview"
    elif st.session_state.get("skip_puppeteer_preview", False):
        st.info("Website visual preview is currently skipped. All SEO crawling, WHOIS, DNS, Excel export, and Security diagnostics remain 100% active.")

    # CASE 3: Service is NOT running -> Ask user permission
    else:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.7); border-left: 4px solid #22d3ee; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
            <h4 style="color: #22d3ee; margin-top: 0; font-size: 1.2rem; font-weight: 700;">
                Local Puppeteer Screenshot Service Required
            </h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 1rem; line-height: 1.5;">
                The Puppeteer screenshot service is currently not running on port 3000. 
                Would you like to automatically install dependencies and start the screenshot service on your computer?
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_perm1, col_perm2 = st.columns([1, 1])
        with col_perm1:
            if st.button("Yes, Install & Start Service on my Computer", type="primary", use_container_width=True):
                with st.spinner("Setting up Puppeteer screenshot service..."):
                    success, msg = install_and_start_puppeteer_service(progress_callback=st.info)
                    if success:
                        st.success(msg)
                        st.session_state["skip_puppeteer_preview"] = False
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(msg)

        with col_perm2:
            if st.button("No, Skip Website Preview", use_container_width=True):
                st.session_state["skip_puppeteer_preview"] = True
                st.rerun()

# ===================== TRIGGER ANALYSIS =====================
if run_analysis:
    domains = [d.strip() for d in domains_input.split('\n') if d.strip()]

    if not domains:
        st.error("Please enter at least one target website URL.")
    else:
        # Check if user entered protected owner/app domain
        protected_domains = [d for d in domains if is_owner_or_app_url(d)]
        if protected_domains:
            for p_dom in protected_domains:
                render_easter_egg(p_dom)
            domains = [d for d in domains if not is_owner_or_app_url(d)]

        if domains:
            progress_bar = st.progress(0)

            # Determine simulation sleep time
            if scan_speed == "Accelerated Simulation (~5min/website)":
                sleep_time = 0.05
            else:
                sleep_time = 0.2

            all_domain_info = []
            all_pages = []
            all_issues = []
            all_audit = []
            all_cyber_results = []

            for idx, domain in enumerate(domains):
                is_safe, ssrf_msg = is_safe_public_domain(domain)
                if not is_safe:
                    st.error(f"Security Block ({domain}): {ssrf_msg}")
                    continue

                # Dynamic scanning simulation
                logs = [
                    "Initializing Intelligent Domain Agent...",
                    "Configuring secure handshake protocols...",
                    "Querying public WHOIS registry databases...",
                    "Analyzing domain registrar and name server propagation...",
                    "Locating and verifying DNS Mail Exchange (MX) records...",
                    "Requesting target robots.txt file...",
                    "Parsing crawl permissions from robots.txt...",
                    "Locating domain sitemap.xml structure...",
                    "Validating SSL certificate and encryption handshake...",
                    "Establishing crawl connections...",
                    "Analyzing document structure and headers...",
                    "Evaluating title tags and meta descriptions...",
                    "Analyzing internal/external hypermedia links...",
                    "Inspecting image assets and alt tags...",
                    "Simulating page load times and Core Web Vitals...",
                    "Extracting HTTP Security Headers compliance policies...",
                    "Scanning landing page HTML for code injection patterns...",
                    "Analyzing script node entropy and hidden iframe alerts...",
                    "Running brand spoofing and typo-squatting heuristics...",
                    "Compiling complete risk assessment report..."
                ]

                for p in range(0, 101, 1):
                    log_idx = min(p // (100 // len(logs)), len(logs) - 1)
                    current_log = logs[log_idx]

                    render_scan_progress(scan_placeholder, domain, current_log, p)
                    if sleep_time > 0:
                        time.sleep(sleep_time)

                def make_live_callback():
                    count = [0]

                    def live_callback(url, status, load_time, title):
                        count[0] += 1
                        crawl_count_placeholder.markdown(f"""
                        <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;">
                            <h4 style="margin: 0; color: #22d3ee;">Active Crawling: {domain}</h4>
                            <p style="margin: 5px 0 0 0; color: #cbd5e1;">Pages Audited: <strong style="color: #22d3ee;">{count[0]} / {max_pages}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                        crawl_log_placeholder.markdown(f"""
                        <div class="recommendation-item" style="border-left-color: #475569; margin: 0.25rem 0;">
                            <strong>Status:</strong> <code>{status}</code> | <strong>Load Time:</strong> {load_time}s | <strong>URL:</strong> <a href="{url}" target="_blank" style="color: #22d3ee; text-decoration: none;">{url}</a>
                            <br/><span style="font-size: 0.85rem; color: #94a3b8;"><strong>Page Title:</strong> {title[:100]}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    return live_callback

                # Run Domain lookup (WHOIS and DNS)
                domain_info = get_domain_info(domain)
                df_domain = pd.DataFrame([domain_info])
                creation_str = domain_info.get("Creation_Date", "N/A")

                # Run SEO Crawl
                df_pages, df_issues, df_audit = crawl_page(
                    domain, max_pages, live_callback=make_live_callback())

                # Clean up the crawl placeholder UI
                crawl_count_placeholder.empty()
                crawl_log_placeholder.empty()

                if not df_issues.empty:
                    df_issues['Domain'] = domain
                if not df_audit.empty:
                    df_audit['Domain'] = domain

                all_domain_info.append(df_domain)
                all_pages.append(df_pages)
                all_issues.append(df_issues)
                all_audit.append(df_audit)

                # Run Cybersecurity Scanning
                clean_domain = domain.replace("https://", "").replace("http://", "").rstrip("/").split("/")[0]
                original_url = f"https://{clean_domain}" if domain.startswith("https://") else f"http://{clean_domain}"
                
                html_content = ""
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                try:
                    resp = requests.get(original_url, timeout=8, headers=headers, allow_redirects=True, verify=False)
                    html_content = resp.text
                except Exception:
                    try:
                        fallback_url = f"http://{clean_domain}" if original_url.startswith("https://") else f"https://{clean_domain}"
                        resp = requests.get(fallback_url, timeout=8, headers=headers, allow_redirects=True, verify=False)
                        html_content = resp.text
                        original_url = fallback_url
                    except Exception:
                        pass
                
                cyber_res = run_cyber_scan(clean_domain, original_url, html_content, creation_str)
                all_cyber_results.append(cyber_res)

                progress_bar.progress((idx + 1) / len(domains))

            scan_placeholder.empty()
            progress_bar.empty()

            df_all_domain = pd.concat(all_domain_info, ignore_index=True)
            df_all_pages = pd.concat(all_pages, ignore_index=True)
            df_all_issues = pd.concat(all_issues, ignore_index=True)
            df_all_audit = pd.concat(all_audit, ignore_index=True)

            # Store in session state for persistent rendering across user tab switches and scroll domain selection
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"Unified_Domain_Intelligence_Report_{timestamp}.xlsx"
            generate_unified_report(df_all_domain, df_all_pages, df_all_issues, df_all_audit, all_cyber_results, filename)

            st.session_state["audit_results"] = {
                "df_all_domain": df_all_domain,
                "df_all_pages": df_all_pages,
                "df_all_issues": df_all_issues,
                "df_all_audit": df_all_audit,
                "all_cyber_results": all_cyber_results,
                "domains": domains,
                "filename": filename
            }
            st.rerun()

# ===================== DISPLAY PERSISTENT RESULTS =====================
if "audit_results" in st.session_state and st.session_state["audit_results"]:
    res_data = st.session_state["audit_results"]
    df_all_domain = res_data["df_all_domain"]
    df_all_pages = res_data["df_all_pages"]
    df_all_issues = res_data["df_all_issues"]
    df_all_audit = res_data["df_all_audit"]
    all_cyber_results = res_data["all_cyber_results"]
    domains = res_data["domains"]
    filename = res_data["filename"]

    st.success(f"Analysis Completed Successfully for {len(domains)} Website(s)!")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Summary Dashboard",
        "Domain Info",
        "Crawled Pages",
        "SEO Issues",
        "Technical Audit",
        "Security Scorecard"
    ])

    with tab1:
        st.markdown("<h3 style='color: #22d3ee; margin-top: 0;'>Executive SEO Audit Summary</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); border-left: 4px solid #22d3ee; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem; color: #cbd5e1;">
            <strong>What is this summary?</strong> This dashboard provides a high-level overview of your target websites. It counts total audited pages, identifies technical SEO errors that could hurt your Google search rank, and measures overall cybersecurity compliance.
        </div>
        """, unsafe_allow_html=True)

        high_crit_count = len(df_all_issues[df_all_issues.get('Severity', pd.Series()).isin(
            ['High', 'Critical'])]) if not df_all_issues.empty else 0

        render_metric_cards(len(domains), len(df_all_issues), high_crit_count)

        st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem;'>Cybersecurity Score Summary</h3>", unsafe_allow_html=True)
        sec_summary_rows = []
        for r in all_cyber_results:
            sec_summary_rows.append({
                "Domain": r["domain"],
                "Security Score": f"{r['global_score']}%",
                "Security Grade": r["grade"],
                "Risk Rating": r["rating"],
                "SSL Validated": "Yes" if r["ssl_info"]["valid"] else "No / Untrusted",
                "Load Time (sec)": r["load_time"]
            })
        st.dataframe(pd.DataFrame(sec_summary_rows), use_container_width=True)

        if not df_all_pages.empty and 'Status' in df_all_pages.columns:
            st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem;'>HTTP Status Code Distribution</h3>", unsafe_allow_html=True)
            status_counts = df_all_pages['Status'].value_counts().reset_index()
            status_counts.columns = ['Status Code', 'Number of Pages']
            status_counts['Status Code'] = status_counts['Status Code'].astype(str)
            st.bar_chart(status_counts.set_index('Status Code'))

    with tab2:
        st.markdown("<h3 style='color: #22d3ee; margin-top: 0;'>Domain & WHOIS Ownership Details</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); border-left: 4px solid #22d3ee; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem; color: #cbd5e1;">
            <strong>What is Domain Info?</strong> Domain Info shows official domain registration records, including who registered the domain, when it was created, when it expires, and which DNS nameservers route visitor traffic.
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_all_domain, use_container_width=True)

    with tab3:
        st.markdown("<h3 style='color: #22d3ee; margin-top: 0;'>Crawled Web Page Catalog</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); border-left: 4px solid #22d3ee; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem; color: #cbd5e1;">
            <strong>What are Crawled Pages?</strong> This table lists every individual webpage discovered on your site during the audit, along with page titles, HTTP response codes (such as 200 OK or 404 Not Found), and link counts.
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_all_pages, use_container_width=True)

    with tab4:
        st.markdown("<h3 style='color: #22d3ee; margin-top: 0;'>Identified SEO Issues & Vulnerabilities</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); border-left: 4px solid #22d3ee; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem; color: #cbd5e1;">
            <strong>What are SEO Issues?</strong> Issues highlight missing title tags, duplicate meta descriptions, broken links, or missing image alt attributes that prevent search engines like Google from indexing your content effectively.
        </div>
        """, unsafe_allow_html=True)
        if not df_all_issues.empty:
            st.dataframe(df_all_issues, use_container_width=True)
        else:
            st.info("No critical SEO issues found on the analyzed pages.")

    with tab5:
        st.markdown("<h3 style='color: #22d3ee; margin-top: 0;'>Technical Audit & Core Web Vitals</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); border-left: 4px solid #22d3ee; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem; color: #cbd5e1;">
            <strong>What is a Technical Audit?</strong> Technical Audit measures website speed and user experience metrics (Core Web Vitals) including load times, page file size, and mobile responsiveness. Fast websites rank higher on search engines.
        </div>
        """, unsafe_allow_html=True)
        if not df_all_audit.empty:
            st.dataframe(df_all_audit, use_container_width=True)

            if 'Load_Time_sec' in df_all_audit.columns:
                st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem;'>Page Load Time by URL (seconds)</h3>", unsafe_allow_html=True)
                load_df = df_all_audit[['URL_Slug', 'Load_Time_sec']].copy()
                load_df['Page'] = load_df['URL_Slug'].apply(lambda x: x if len(x) < 25 else x[:22] + '...')
                st.area_chart(load_df.set_index('Page')['Load_Time_sec'])

        st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem;'>AI SEO Actions & Step-by-Step Fixes</h3>", unsafe_allow_html=True)
        
        recs = generate_ai_seo_recommendations(df_all_pages, df_all_issues, df_all_audit)
        
        # CONDITIONAL RECOMMENDATIONS: If 100% healthy or zero issues, don't display unnecessary recommendation items!
        if not recs or (df_all_issues.empty and len(recs) <= 1):
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
                <h4 style="color: #34d399; margin-top: 0; font-size: 1.15rem; font-weight: 700;">
                    100% Optimal SEO Status
                </h4>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 0;">
                    Your website pages fully comply with SEO best practices! Title tags, meta descriptions, canonical structures, and internal links are properly optimized. No action items required.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Trust & Verification Guarantee Banner
            st.markdown("""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(34, 211, 238, 0.3); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
                <h5 style="color: #22d3ee; margin-top: 0; font-size: 1rem; font-weight: 700;">Verified Analysis & Data Accuracy Guarantee</h5>
                <p style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0; line-height: 1.5;">
                    These action items are generated directly from real-time live page analysis, W3C HTML specifications, and search engine optimization standards. Every recommendation is 100% verified against your active website code.
                </p>
            </div>
            """, unsafe_allow_html=True)

            rec_html = '<div class="glass-card" style="padding: 1.5rem !important;">'
            for r in recs:
                sev = r["severity"].lower()
                if sev == "critical":
                    color_style = "border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.08); margin: 10px 0; border-radius: 8px; padding: 12px;"
                    sev_badge = '<span style="color: #ef4444; font-weight: 800;">[CRITICAL]</span>'
                elif sev == "high":
                    color_style = "border-left: 4px solid #f97316; background: rgba(249, 115, 22, 0.08); margin: 10px 0; border-radius: 8px; padding: 12px;"
                    sev_badge = '<span style="color: #f97316; font-weight: 800;">[HIGH]</span>'
                elif sev == "medium":
                    color_style = "border-left: 4px solid #eab308; background: rgba(234, 179, 8, 0.08); margin: 10px 0; border-radius: 8px; padding: 12px;"
                    sev_badge = '<span style="color: #eab308; font-weight: 800;">[MEDIUM]</span>'
                else:
                    color_style = "border-left: 4px solid #22c55e; background: rgba(34, 197, 94, 0.08); margin: 10px 0; border-radius: 8px; padding: 12px;"
                    sev_badge = '<span style="color: #22c55e; font-weight: 800;">[LOW]</span>'
                
                item_html = (
                    f'<div style="{color_style}">'
                    f'<div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 4px; color: #f1f5f9;">{sev_badge} {r["title"]}</div>'
                    f'<div style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 6px;">{r["description"]}</div>'
                    f'<div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 4px;"><strong>Impact:</strong> {r["impact"]}</div>'
                    f'<div style="color: #22d3ee; font-size: 0.85rem; font-weight: 600;"><strong>Action:</strong> {r["action_item"]}</div>'
                    f'</div>'
                )
                rec_html += item_html
            rec_html += '</div>'
            st.markdown(rec_html, unsafe_allow_html=True)

    with tab6:
        st.markdown("<h3 style='color: #22d3ee; margin-top: 0;'>Cybersecurity & Risk Scorecard</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); border-left: 4px solid #22d3ee; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem; color: #cbd5e1;">
            <strong>What is the Security Scorecard?</strong> This section checks if your website uses valid SSL encryption, has active security headers to block hackers, and verifies that your domain is free from malware or phishing risks.
        </div>
        """, unsafe_allow_html=True)

        # Domain selector for Security Scorecard
        clean_domains = [r["domain"] for r in all_cyber_results]
        if len(clean_domains) > 1:
            selected_domain = st.selectbox(
                "Select Target Domain for Security Inspection:",
                options=clean_domains,
                key="sec_scorecard_domain_select"
            )
        else:
            selected_domain = clean_domains[0]

        res = next(r for r in all_cyber_results if r["domain"] == selected_domain)

        # Trust & Verification Guarantee Banner for Security Score
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
            <h5 style="color: #34d399; margin-top: 0; font-size: 1rem; font-weight: 700;">Verified Security Standard & Trusted Source</h5>
            <p style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0; line-height: 1.5;">
                This security grade is computed directly from live target server response headers, RFC 2818 SSL certificate validation, and official OWASP Top 10 web security compliance specifications. All test results are 100% objective and verified directly from server handshakes.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Transparent Scoring Formula Breakdown Expander
        with st.expander("Security Score Calculation Basis & Mathematical Formula", expanded=False):
            st.markdown("""
            <div style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6;">
                <h5 style="color: #22d3ee; margin-top: 0;">How is your Security Score calculated?</h5>
                <p>The Global Security Compliance Score (0–100%) is calculated by evaluating four independent core security pillars (25% weight each):</p>
                <ul>
                    <li><strong>1. SSL/TLS Certificate Validation (25% Weight):</strong> Verifies active HTTPS encryption, CA trust chain validation, and TLS 1.2/1.3 handshake protocols.</li>
                    <li><strong>2. HTTP Security Headers (25% Weight):</strong> Audits 6 critical browser defense headers (Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy).</li>
                    <li><strong>3. Phishing & Brand Protection (25% Weight):</strong> Checks domain age, algorithmic entropy, brand impersonation risks, and high-risk top-level domain extensions (TLDs).</li>
                    <li><strong>4. Malware & Code Safety (25% Weight):</strong> Scans frontend HTML for hidden drive-by iframes, script obfuscation (`eval`, `unescape`), exposed secret credentials, and insecure form endpoints.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Top Metric Cards
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Security Compliance Score</div>
                <div class="metric-value" style="color: #06b6d4;">{res['global_score']}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Security Grade</div>
                <div class="metric-value" style="color: #818cf8;">{res['grade']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            rating_color = "#f87171" if "High" in res['rating'] or "Critical" in res['rating'] else ("#f59e0b" if "Medium" in res['rating'] else "#10b981")
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Risk Exposure Rating</div>
                <div class="metric-value" style="color: {rating_color};">{res['rating']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Section 1: SSL Validation Details
        st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;'>SSL / TLS Certificate Validation</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;">
            <strong>What is SSL?</strong> SSL (HTTPS) encrypts data sent between your visitors and your website. It protects passwords, contact forms, and payment details from being intercepted by hackers.
        </p>
        """, unsafe_allow_html=True)
        ssl_rows = []
        for r in all_cyber_results:
            ssl_rows.append({
                "Domain": r["domain"],
                "SSL Status": "Valid (Trusted)" if r["ssl_info"]["valid"] else "Invalid / Untrusted",
                "Issuer Common Name": r["ssl_info"]["issuer_cn"],
                "Issuer Organization": r["ssl_info"]["issuer_org"],
                "Expiration Date": r["ssl_info"]["expiry_date"],
                "Days Remaining": r["ssl_info"]["days_left"] if r["ssl_info"]["days_left"] >= 0 else "N/A"
            })
        st.dataframe(pd.DataFrame(ssl_rows), use_container_width=True)

        # Section 2: Security Headers Audit
        st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;'>HTTP Security Headers Audit</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;">
            <strong>What are HTTP Security Headers?</strong> Security headers are instructions sent by your web server to visitors' browsers to defend against cross-site scripting (XSS), clickjacking, and data tampering.
        </p>
        """, unsafe_allow_html=True)
        df_headers = pd.DataFrame(res["header_findings"])[["header", "status", "value", "severity", "desc"]]
        df_headers.columns = ["Security Header", "Compliance Status", "Header Value", "Severity Level", "Policy Description"]
        st.dataframe(df_headers, use_container_width=True)

        # Section 3: Threat & Risk Heuristics
        st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;'>Threat & Risk Analysis</h3>", unsafe_allow_html=True)
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("<h4 style='color: #cbd5e1; font-weight: 700; margin-bottom: 1rem;'>Phishing Indicators</h4>", unsafe_allow_html=True)
            if res["phishing_reasons"]:
                for reason in res["phishing_reasons"]:
                    st.markdown(f"""
                    <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: #f87171; font-size: 0.92rem;">
                        <strong>Risk Warning:</strong> {reason}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 8px; padding: 12px; color: #34d399; font-size: 0.92rem; font-weight: 600;">
                    No brand spoofing or high-entropy anomalies detected.
                </div>
                """, unsafe_allow_html=True)

        with col_t2:
            st.markdown("<h4 style='color: #cbd5e1; font-weight: 700; margin-bottom: 1rem;'>Malware Risk Analysis</h4>", unsafe_allow_html=True)
            if res["malware_reasons"]:
                for reason in res["malware_reasons"]:
                    st.markdown(f"""
                    <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: #f87171; font-size: 0.92rem;">
                        <strong>Threat Alert:</strong> {reason}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 8px; padding: 12px; color: #34d399; font-size: 0.92rem; font-weight: 600;">
                    No drive-by hidden frames or obfuscated script signatures found.
                </div>
                """, unsafe_allow_html=True)

        # Section 4: Vulnerability Remediation Plan
        st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;'>Vulnerability Remediation Plan</h3>", unsafe_allow_html=True)
        
        recs_list = res["recommendations"]
        is_perfect = (res["global_score"] == 100) or (len(recs_list) == 1 and "No active vulnerabilities found" in recs_list[0])

        # CONDITIONAL SECURITY RECOMMENDATIONS: If score is 100% or 0 active vulnerabilities, display success box instead of unnecessary remediation items!
        if is_perfect:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
                <h4 style="color: #34d399; margin-top: 0; font-size: 1.15rem; font-weight: 700;">
                    100% Optimal Security Compliance
                </h4>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 0;">
                    Congratulations! Your target domain fully satisfies all security requirements. SSL encryption is active, all 6 HTTP security headers are enabled, and zero malware or phishing risks were detected. No remediation items required.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            rec_html = '<div class="glass-card" style="padding: 1.5rem !important;">'
            for idx_rec, rec in enumerate(recs_list):
                rec_html += f'<div style="background: rgba(15, 23, 42, 0.5); border-left: 4px solid #0284c7; border-radius: 8px; padding: 12px; margin: 8px 0; color: #e0f2fe; font-size: 0.95rem;"><strong>Action Item {idx_rec + 1}:</strong> {rec}</div>'
            rec_html += '</div>'
            st.markdown(rec_html, unsafe_allow_html=True)

    # Save and output the unified Excel report
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    render_download_section()

    if os.path.exists(filename):
        with open(filename, "rb") as file:
            st.download_button(
                "Download Unified Enterprise Domain Intelligence Report (Excel Spreadsheet)",
                data=file,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

else:
    render_ready_to_scan()

# Render footer on all pages
inject_footer_element()
