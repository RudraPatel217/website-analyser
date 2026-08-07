import sys
import os
# Ensure the current directory is in sys.path so modules resolve correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time
import base64
from urllib.parse import quote
from config import GTMETRIX_API_KEY, BUILTWITH_API_KEY

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
    get_gtmetrix_screenshot,
    get_domain_info,
    crawl_page,
    generate_excel_report,
    generate_security_report,
    run_cyber_scan,
    generate_ai_seo_recommendations,
    generate_unified_report,
    is_safe_public_domain,
    check_service_health,
    install_and_start_puppeteer_service
)

st.set_page_config(page_title="SEO Domain Intelligence Agent", layout="wide")

# Inject global style and header
inject_premium_styles()
inject_header_element()

# Input Panel configured inside native bordered container
with st.container(border=True):
    st.markdown(
        "<h3 style='margin-top: 0; color: #22d3ee; font-weight: 700; font-size: 1.3rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;'>Configuration Panel</h3>",
        unsafe_allow_html=True)
    domains_input = st.text_area("Target Website URLs (one domain per line):",
                                 value="https://jeenweb.com",
                                 height=100)
    
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
            index=default_source_index
        )
    with col_c1:
        max_pages = st.slider("Max crawl depth pages per domain:", 5, 300, 25)
    with col_c2:
        scan_speed = st.selectbox(
            "Scan Speed / Simulation Delay:",
            options=[
                "Accelerated Simulation (~5min/website)",
                "Thorough Deep Scan (~10min/website)"],
            index=1
        )

    # Secure API Key Overrides for Visitors / Users
    with st.expander("🔑 API Key Settings (Optional - Use Your Own Keys)", expanded=False):
        st.markdown(
            "<p style='color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0.75rem;'>"
            "To protect admin keys and quota, you can supply your personal API keys below. "
            "If left blank, the app will use server defaults or free public APIs (Microlink / WordPress mShot) automatically."
            "</p>",
            unsafe_allow_html=True
        )
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            user_gtmetrix_key = st.text_input(
                "Personal GTmetrix API Key:",
                type="password",
                placeholder="Paste your GTmetrix API Key...",
                help="Sign up and obtain your free API key at https://gtmetrix.com/api/"
            )
        with col_k2:
            user_builtwith_key = st.text_input(
                "Personal BuiltWith API Key:",
                type="password",
                placeholder="Paste your BuiltWith API Key...",
                help="Sign up and obtain your API key at https://builtwith.com/api"
            )

    # Determine active API keys (User UI input takes priority over server environment keys)
    active_gtmetrix_key = user_gtmetrix_key.strip() if user_gtmetrix_key.strip() else GTMETRIX_API_KEY.strip()
    active_builtwith_key = user_builtwith_key.strip() if user_builtwith_key.strip() else BUILTWITH_API_KEY.strip()

    # Session state for tracking user choice on skipping preview
    if "skip_puppeteer_preview" not in st.session_state:
        st.session_state["skip_puppeteer_preview"] = False

run_analysis = st.button(
    "Start Full Multi-Website Analysis",
    type="primary",
    use_container_width=True)

scan_placeholder = st.empty()
crawl_count_placeholder = st.empty()
crawl_log_placeholder = st.empty()

# Check local Puppeteer service status
service_active, _ = check_service_health()

# ===================== HOMEPAGE PREVIEW =====================
if domains_input.strip():
    st.markdown("### 🌐 Homepage Previews")

    # CASE 1: Service is ALREADY running on port 3000 -> Render preview directly with ZERO message/prompt!
    if service_active:
        for domain in domains_input.split('\n'):
            domain = domain.strip()
            if domain:
                try:
                    # SSRF Protection Check
                    is_safe, ssrf_msg = is_safe_public_domain(domain)
                    if not is_safe:
                        st.error(f"🛡️ Security Block ({domain}): {ssrf_msg}")
                        continue

                    screenshot_url = f"http://localhost:3000/screenshot?url={quote(domain)}"
                    render_browser_preview(domain, screenshot_url)
                except Exception as e:
                    st.warning(f"Could not preview {domain}: {str(e)}")

    # CASE 2: Service is NOT running, but user selected "No, Skip Website Preview"
    elif st.session_state.get("skip_puppeteer_preview", False):
        st.info("ℹ️ Website visual preview is currently skipped. All SEO crawling, WHOIS, DNS, Excel export, and Security diagnostics remain 100% active.")

    # CASE 3: Service is NOT running -> Ask user permission to install & start Puppeteer service on their laptop
    else:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.7); border-left: 4px solid #22d3ee; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
            <h4 style="color: #22d3ee; margin-top: 0; font-size: 1.2rem; font-weight: 700;">
                🌐 Local Puppeteer Screenshot Service Required
            </h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 1rem; line-height: 1.5;">
                The Puppeteer screenshot service is currently not running on your laptop (port 3000). 
                Would you like to automatically install dependencies and start the screenshot service on your laptop?
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_perm1, col_perm2 = st.columns([1, 1])
        with col_perm1:
            if st.button("⚡ Yes, Install & Start Service on my Laptop", type="primary", use_container_width=True):
                with st.spinner("Setting up Puppeteer screenshot service on your machine..."):
                    success, msg = install_and_start_puppeteer_service(progress_callback=st.info)
                    if success:
                        st.success(msg)
                        st.session_state["skip_puppeteer_preview"] = False
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(msg)

        with col_perm2:
            if st.button("❌ No, Skip Website Preview", use_container_width=True):
                st.session_state["skip_puppeteer_preview"] = True
                st.rerun()


# ===================== MAIN ANALYSIS =====================
if run_analysis:
    domains = [d.strip() for d in domains_input.split('\n') if d.strip()]

    if not domains:
        st.error("Please enter at least one domain")
    else:
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
                st.error(f"🛡️ Target Security Block ({domain}): {ssrf_msg}")
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
        
        st.success(f"Analysis Completed for {len(domains)} Websites!")

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Summary Dashboard",
            "Domain Info",
            "Crawled Pages",
            "SEO Issues",
            "Technical Audit",
            "Security Scorecard"
        ])

        with tab1:
            high_crit_count = len(df_all_issues[df_all_issues.get('Severity', pd.Series()).isin(
                ['High', 'Critical'])]) if not df_all_issues.empty else 0

            st.markdown("<h3 style='color: #22d3ee; margin-top: 0;'>SEO Audit Summary</h3>", unsafe_allow_html=True)
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
                st.markdown(
                    "<h3 style='color: #22d3ee; margin-top: 2rem;'>HTTP Status Code Distribution</h3>",
                    unsafe_allow_html=True)
                status_counts = df_all_pages['Status'].value_counts(
                ).reset_index()
                status_counts.columns = ['Status Code', 'Number of Pages']
                status_counts['Status Code'] = status_counts['Status Code'].astype(
                    str)
                st.bar_chart(status_counts.set_index('Status Code'))

        with tab2:
            st.dataframe(df_all_domain, use_container_width=True)
        with tab3:
            st.dataframe(df_all_pages, use_container_width=True)
        with tab4:
            if not df_all_issues.empty:
                st.dataframe(df_all_issues, use_container_width=True)
            else:
                st.info("No issues found")

        with tab5:
            st.markdown(
                "<h3 style='color: #22d3ee; margin-top: 1.5rem;'>Technical Audit + Core Web Vitals</h3>",
                unsafe_allow_html=True)
            if not df_all_audit.empty:
                st.dataframe(df_all_audit, use_container_width=True)

                if 'Load_Time_sec' in df_all_audit.columns:
                    st.markdown(
                        "<h3 style='color: #22d3ee; margin-top: 2rem;'>Page Load Time by URL (seconds)</h3>",
                        unsafe_allow_html=True)
                    load_df = df_all_audit[[
                        'URL_Slug', 'Load_Time_sec']].copy()
                    load_df['Page'] = load_df['URL_Slug'].apply(
                        lambda x: x if len(x) < 25 else x[:22] + '...')
                    st.area_chart(load_df.set_index('Page')['Load_Time_sec'])

            st.markdown(
                "<h3 style='color: #22d3ee; margin-top: 2rem;'>AI SEO Actions & Recommendations</h3>",
                unsafe_allow_html=True)
            
            recs = generate_ai_seo_recommendations(df_all_pages, df_all_issues, df_all_audit)
            
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
            # Domain selector for Security Scorecard
            clean_domains = [r["domain"] for r in all_cyber_results]
            if len(clean_domains) > 1:
                selected_domain = st.selectbox("Select Target Domain for Security Scorecard:", options=clean_domains, key="sec_scorecard_sel")
            else:
                selected_domain = clean_domains[0]

            res = next(r for r in all_cyber_results if r["domain"] == selected_domain)

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
            st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;'>🔒 SSL / TLS Certificate Validation</h3>", unsafe_allow_html=True)
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
            st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;'>🛡️ HTTP Security Headers Audit</h3>", unsafe_allow_html=True)
            df_headers = pd.DataFrame(res["header_findings"])[["header", "status", "value", "severity", "desc"]]
            df_headers.columns = ["Security Header", "Compliance Status", "Header Value", "Severity Level", "Policy Description"]
            st.dataframe(df_headers, use_container_width=True)

            # Section 3: Threat & Risk Heuristics
            st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;'>⚠️ Threat & Risk Heuristics</h3>", unsafe_allow_html=True)
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown("<h4 style='color: #cbd5e1; font-weight: 700; margin-bottom: 1rem;'>🎣 Phishing Indicators</h4>", unsafe_allow_html=True)
                if res["phishing_reasons"]:
                    for reason in res["phishing_reasons"]:
                        st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: #f87171; font-size: 0.92rem;">
                            <strong>⚠️ Risk Warning:</strong> {reason}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 8px; padding: 12px; color: #34d399; font-size: 0.92rem; font-weight: 600;">
                        ✓ No brand spoofing or high-entropy anomalies detected.
                    </div>
                    """, unsafe_allow_html=True)

            with col_t2:
                st.markdown("<h4 style='color: #cbd5e1; font-weight: 700; margin-bottom: 1rem;'>👾 Malware Risk Analysis</h4>", unsafe_allow_html=True)
                if res["malware_reasons"]:
                    for reason in res["malware_reasons"]:
                        st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: #f87171; font-size: 0.92rem;">
                            <strong>⚠️ Threat Alert:</strong> {reason}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 8px; padding: 12px; color: #34d399; font-size: 0.92rem; font-weight: 600;">
                        ✓ No drive-by hidden frames or obfuscated script signatures found.
                    </div>
                    """, unsafe_allow_html=True)

            # Section 4: Vulnerability Remediation Plan
            st.markdown("<h3 style='color: #22d3ee; margin-top: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;'>📋 Vulnerability Remediation Plan</h3>", unsafe_allow_html=True)
            rec_html = '<div class="glass-card" style="padding: 1.5rem !important;">'
            for idx_rec, rec in enumerate(res["recommendations"]):
                rec_html += f'<div style="background: rgba(15, 23, 42, 0.5); border-left: 4px solid #0284c7; border-radius: 8px; padding: 12px; margin: 8px 0; color: #e0f2fe; font-size: 0.95rem;"><strong>Action Item {idx_rec + 1}:</strong> {rec}</div>'
            rec_html += '</div>'
            st.markdown(rec_html, unsafe_allow_html=True)

        # Save and output the unified Excel report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"Unified_Domain_Intelligence_Report_{timestamp}.xlsx"

        generate_unified_report(df_all_domain, df_all_pages, df_all_issues, df_all_audit, all_cyber_results, filename)

        st.markdown(
            "<div style='margin-top: 2rem;'></div>",
            unsafe_allow_html=True)
        
        render_download_section()

        with open(filename, "rb") as file:
            st.download_button(
                "Download Unified Enterprise Domain Intelligence Report (9 Sheets)",
                data=file,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

else:
    render_ready_to_scan()

# Render footer on all pages
inject_footer_element()
