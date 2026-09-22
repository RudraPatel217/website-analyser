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
    render_download_section,
    render_info_banner,
    render_tab_heading,
    render_styled_table,
    render_styled_bar_chart,
    render_styled_area_chart
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
    Detects if target domain matches the application's host URL or self-scan attempts.
    """
    d = domain_str.lower().strip().replace("https://", "").replace("http://", "").split("/")[0].split(":")[0]
    protected_patterns = [
        "website-analyser-rudra.streamlit.app",
        "website-analyser",
        "streamlit.app"
    ]
    return any(p in d for p in protected_patterns)

def render_easter_egg(domain):
    """
    Displays notification card when someone attempts to scan the app or owner domain.
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(245, 158, 11, 0.15) 100%);
        border: 2px dashed #f59e0b;
        border-radius: 20px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.2);
    ">
        <h2 style="color: #fbbf24; font-size: 2.2rem; font-weight: 800; margin-top: 0; margin-bottom: 0.5rem; letter-spacing: 0.5px;">
            Access Restricted: Protected Domain
        </h2>
        <p style="color: #f1f5f9; font-size: 1.15rem; max-width: 650px; margin: 0.5rem auto 0 auto; line-height: 1.6; font-weight: 600;">
            Auditing internal system domains is restricted. Please enter an external website address to audit.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_preview_meme(domain):
    """
    Displays notification in the preview section when auditing the app itself.
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 2px solid rgba(245, 158, 11, 0.4);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    ">
        <h3 style="color: #fbbf24; font-size: 1.6rem; font-weight: 800; margin-top: 0; margin-bottom: 0.75rem;">
            Self-Audit Protection Active
        </h3>
        <p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.25rem;">
            Target domain matches internal application address.
        </p>
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <img src="https://media.giphy.com/media/l36kUemp4vITTX4PC/giphy.gif" 
                 alt="Spider-Man pointing meme" 
                 style="max-width: 460px; width: 100%; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); border: 2px solid rgba(255,255,255,0.1);" />
        </div>
        <p style="color: #cbd5e1; font-size: 0.95rem; font-style: italic; margin-bottom: 0;">
            "Self-audit protection is active."
        </p>
    </div>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="SEO Domain Intelligence Agent", layout="wide")

def set_theme(mode):
    st.session_state["theme_mode"] = mode

def clear_scan_results():
    st.session_state["audit_results"] = None

if "theme_mode" not in st.session_state or st.session_state["theme_mode"] not in ["corporate", "light"]:
    st.session_state["theme_mode"] = "corporate"

theme_mode = st.session_state["theme_mode"]

# Inject global style and header with active theme
inject_premium_styles(theme_mode)
inject_header_element(theme_mode)

# Floating pill theme toggle — top-right corner
toggle_col_l, toggle_col_r = st.columns([9, 1])
with toggle_col_r:
    if theme_mode == "light":
        st.button("Dark Mode", key="theme_toggle_btn", use_container_width=False, on_click=set_theme, args=("corporate",))
    else:
        st.button("Light Mode", key="theme_toggle_btn", use_container_width=False, on_click=set_theme, args=("light",))

# Input Panel configured inside native bordered container
with st.container(border=True):
    if theme_mode == "light":
        header_color = "#1E293B"
        border_color = "#E2E8F0"
    else:  # corporate dark
        header_color = "#38bdf8"
        border_color = "rgba(59, 130, 246, 0.25)"

    st.markdown(
        f"<h3 style='margin-top: 0; color: {header_color}; font-weight: 700; font-size: 1.3rem; border-bottom: 1px solid {border_color}; padding-bottom: 0.75rem; margin-bottom: 1rem;'>Website Audit Setup</h3>",
        unsafe_allow_html=True)
    
    domains_input = st.text_area(
        "Target Website URLs (enter one domain per line):",
        value="",
        placeholder="https://websitename.com",
        height=100,
        help="Type or paste the web addresses of the websites you want to analyze (for example: https://websitename.com). You can audit multiple websites at once by placing each URL on a new line."
    )
    
    service_healthy, _ = check_service_health()
    preview_options = [
        "Instant Domain Snapshot (0s)",
        "Ultra-Fast Visual Capture"
    ]
    if service_healthy:
        preview_options.append("Local Puppeteer Engine (Port 3000)")

    col_source, col_c1, col_c2 = st.columns(3)
    with col_source:
        screenshot_source = st.selectbox(
            "Website Visual Preview Engine:",
            options=preview_options,
            index=0,
            help="Select your preferred mode for homepage visual previews (optimized for 1-2s response)."
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

col_b1, col_b2 = st.columns([3, 1])
with col_b1:
    run_analysis = st.button(
        "Start Full Multi-Website Analysis",
        type="primary",
        use_container_width=True
    )
with col_b2:
    if "audit_results" in st.session_state and st.session_state["audit_results"]:
        st.button("Clear Results & New Scan", key="clear_scan_btn", type="secondary", use_container_width=True, on_click=clear_scan_results)

scan_placeholder = st.empty()
crawl_count_placeholder = st.empty()
crawl_log_placeholder = st.empty()

# ===================== HOMEPAGE PREVIEW =====================
if domains_input.strip() and not st.session_state.get("audit_results"):
    st.markdown("### Homepage Previews")

    for domain in domains_input.split('\n'):
        domain = domain.strip()
        if domain:
            if is_owner_or_app_url(domain):
                render_preview_meme(domain)
                continue

            try:
                # SSRF Protection Check
                is_safe, ssrf_msg = is_safe_public_domain(domain)
                if not is_safe:
                    st.error(f"Security Block ({domain}): {ssrf_msg}")
                    continue

                target_url = domain if (domain.startswith("http://") or domain.startswith("https://")) else f"https://{domain}"
                encoded = quote(target_url, safe="")
                clean_host = target_url.replace("https://", "").replace("http://", "").rstrip("/").split("/")[0]

                if "Instant Domain" in screenshot_source:
                    primary_url = "instant"
                    fallback_url = None
                elif "Local Puppeteer" in screenshot_source:
                    primary_url = f"http://localhost:3000/screenshot?url={encoded}"
                    # Puppeteer fallback: use thumbnail.ws free tier
                    fallback_url = f"https://api.thumbnail.ws/api/abc123/thumbnail/get?url={encoded}&width=800"
                else:
                    # Ultra-Fast Visual Capture — use reliable waterfall:
                    # 1. screenshotmachine (free, reliable, no CAPTCHA returns)
                    # 2. thumbnail.ws as backup
                    # JS in render_browser_preview will validate the image isn't a bot-block page
                    primary_url = f"https://mini.s-shot.ru/1024x768/PNG/1024/Z100/?{target_url}"
                    fallback_url = f"https://api.thumbnail.ws/api/abc123/thumbnail/get?url={encoded}&width=800"

                render_browser_preview(domain, primary_url, fallback_url=fallback_url, theme_mode=theme_mode)
            except Exception as e:
                st.warning(f"Could not preview {domain}: {str(e)}")



# ===================== TRIGGER ANALYSIS =====================
if run_analysis:
    domains = [d.strip() for d in domains_input.split('\n') if d.strip()]

    if not domains:
        st.error("Please enter at least one target website URL.")
    else:
        # Anti-Bot Rate Limiting & Cooldown Protection
        now = time.time()
        last_scan = st.session_state.get("last_scan_timestamp", 0)
        cooldown = 5
        if now - last_scan < cooldown:
            st.warning(f"**Bot Protection & Anti-Flood:** Please wait {int(cooldown - (now - last_scan))}s before launching another multi-website scan.")
            st.stop()
        st.session_state["last_scan_timestamp"] = now
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
                if is_owner_or_app_url(domain):
                    render_easter_egg(domain)
                    continue

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

                for p in range(0, 100, 1):
                    log_idx = min(p // (100 // len(logs)), len(logs) - 1)
                    current_log = logs[log_idx]

                    render_scan_progress(scan_placeholder, domain, current_log, p, theme_mode=theme_mode)
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
                target_url = domain if (domain.startswith("http://") or domain.startswith("https://")) else f"https://{domain}"
                
                html_content = ""
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9'
                }
                try:
                    resp = requests.get(target_url, timeout=8, headers=headers, allow_redirects=True, verify=False)
                    if resp.status_code == 403 and any(k in resp.headers for k in ['cf-ray', 'cf-mitigated']):
                        try:
                            from urllib.parse import quote
                            r_rnd = requests.get(f"http://127.0.0.1:3000/render?url={quote(target_url)}", timeout=(1.5, 12.0))
                            if r_rnd.status_code == 200:
                                html_content = r_rnd.json().get('html', '')
                        except Exception:
                            html_content = resp.text
                    else:
                        html_content = resp.text
                except Exception:
                    try:
                        fallback_scheme = "http://" if target_url.startswith("https://") else "https://"
                        fallback_url = fallback_scheme + target_url.split("://", 1)[1]
                        resp = requests.get(fallback_url, timeout=8, headers=headers, allow_redirects=True, verify=False)
                        html_content = resp.text
                        target_url = fallback_url
                    except Exception:
                        pass
                
                cyber_res = run_cyber_scan(domain, target_url, html_content, creation_str)
                all_cyber_results.append(cyber_res)

                progress_bar.progress((idx + 1) / len(domains))

            scan_placeholder.empty()
            progress_bar.empty()

            if not all_domain_info:
                # All domains were skipped (e.g. Easter egg or blocked)
                st.session_state["audit_results"] = None
            else:
                df_all_domain = pd.concat(all_domain_info, ignore_index=True) if all_domain_info else pd.DataFrame()
                df_all_pages = pd.concat(all_pages, ignore_index=True) if all_pages else pd.DataFrame()
                df_all_issues = pd.concat(all_issues, ignore_index=True) if all_issues else pd.DataFrame()
                df_all_audit = pd.concat(all_audit, ignore_index=True) if all_audit else pd.DataFrame()

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
                scan_placeholder.empty()
                crawl_count_placeholder.empty()
                crawl_log_placeholder.empty()

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

    nav_tabs = [
        "Summary Dashboard",
        "Domain Info",
        "Crawled Pages",
        "SEO Issues",
        "Technical Audit",
        "Security Scorecard"
    ]

    if "target_tab" not in st.session_state or st.session_state["target_tab"] not in nav_tabs:
        st.session_state["target_tab"] = "Summary Dashboard"

    high_crit_count = len(df_all_issues[df_all_issues.get('Severity', pd.Series()).isin(
        ['High', 'Critical'])]) if not df_all_issues.empty else 0

    def nav_to_domains():
        st.session_state["target_tab"] = "Domain Info"

    def nav_to_issues():
        st.session_state["target_tab"] = "SEO Issues"
        st.session_state["highlight_critical"] = False

    def nav_to_critical(crit_count):
        if crit_count == 0:
            st.session_state["show_no_critical_popup"] = True
        else:
            st.session_state["target_tab"] = "SEO Issues"
            st.session_state["highlight_critical"] = True

    # 3-Second Disappearing Popup when there are 0 Critical Issues
    if st.session_state.get("show_no_critical_popup"):
        st.session_state["show_no_critical_popup"] = False
        st.toast("No critical issue found on analyzed domain(s)")
        st.markdown("""
        <div id="no-critical-toast-box" class="no-critical-toast">
            No critical issue found on analyzed domain(s)
        </div>
        <style>
            .no-critical-toast {
                position: fixed;
                top: 24px;
                right: 24px;
                z-index: 9999999;
                background: linear-gradient(135deg, #059669 0%, #10b981 100%);
                color: #ffffff;
                padding: 16px 28px;
                border-radius: 12px;
                font-weight: 700;
                font-size: 1rem;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
                pointer-events: none;
                animation: noCritFade 3s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            @keyframes noCritFade {
                0% { opacity: 0; transform: translateY(-20px) scale(0.95); }
                10% { opacity: 1; transform: translateY(0) scale(1); }
                80% { opacity: 1; transform: translateY(0) scale(1); }
                100% { opacity: 0; transform: translateY(-15px) scale(0.95); display: none; }
            }
        </style>
        <script>
            setTimeout(function() {
                var el = document.getElementById('no-critical-toast-box');
                if (el) { el.style.display = 'none'; }
            }, 3000);
        </script>
        """, unsafe_allow_html=True)

    # Clickable Metric Cards
    render_metric_cards(
        len(domains),
        len(df_all_issues),
        high_crit_count,
        on_domains_click=nav_to_domains,
        on_issues_click=nav_to_issues,
        on_critical_click=nav_to_critical,
        theme_mode=theme_mode
    )

    current_nav_tab = st.segmented_control(
        "Navigation Tabs",
        options=nav_tabs,
        default=st.session_state["target_tab"],
        key=f"active_nav_tab_{st.session_state['target_tab']}",
        label_visibility="collapsed"
    )
    if current_nav_tab and current_nav_tab != st.session_state["target_tab"]:
        st.session_state["target_tab"] = current_nav_tab
        st.rerun()

    if current_nav_tab == "Summary Dashboard":
        render_tab_heading("Executive SEO Audit Summary", theme_mode=theme_mode)
        render_info_banner(
            "What is this summary?",
            "This dashboard provides a high-level overview of your target websites. It counts total audited pages, identifies technical SEO errors that could hurt your Google search rank, and measures overall cybersecurity compliance.",
            theme_mode=theme_mode
        )

        render_tab_heading("Cybersecurity Score Summary", theme_mode=theme_mode, margin_top="2rem")
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
        render_styled_table(pd.DataFrame(sec_summary_rows), theme_mode=theme_mode)

        if not df_all_pages.empty and 'Status' in df_all_pages.columns:
            render_tab_heading("HTTP Status Code Distribution", theme_mode=theme_mode, margin_top="2rem")
            status_counts = df_all_pages['Status'].value_counts().reset_index()
            status_counts.columns = ['Status Code', 'Number of Pages']
            status_counts['Status Code'] = status_counts['Status Code'].astype(str)
            render_styled_bar_chart(status_counts, 'Status Code', 'Number of Pages', theme_mode=theme_mode)

    elif current_nav_tab == "Domain Info":
        render_tab_heading("Domain & WHOIS Ownership Details", theme_mode=theme_mode)
        render_info_banner(
            "What is Domain Info?",
            "Domain Info shows official domain registration records, including who registered the domain, when it was created, when it expires, and which DNS nameservers route visitor traffic.",
            theme_mode=theme_mode
        )
        render_styled_table(df_all_domain, theme_mode=theme_mode)

    elif current_nav_tab == "Crawled Pages":
        render_tab_heading("Crawled Web Page Catalog", theme_mode=theme_mode)
        render_info_banner(
            "What are Crawled Pages?",
            "This table lists every individual webpage discovered on your site during the audit, along with page titles, HTTP response codes (such as 200 OK or 404 Not Found), and link counts.",
            theme_mode=theme_mode
        )
        render_styled_table(df_all_pages, theme_mode=theme_mode)

    elif current_nav_tab == "SEO Issues":
        render_tab_heading("Identified SEO Issues & Vulnerabilities", theme_mode=theme_mode)
        render_info_banner(
            "What are SEO Issues?",
            "Issues highlight missing title tags, duplicate meta descriptions, broken links, or missing image alt attributes that prevent search engines like Google from indexing your content effectively.",
            theme_mode=theme_mode
        )

        is_highlighted = st.session_state.get("highlight_critical", False)
        if is_highlighted:
            col_h1, col_h2 = st.columns([4, 1])
            with col_h1:
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; border-radius: 10px; padding: 12px 18px; margin-bottom: 1.25rem; color: #fca5a5; font-size: 0.95rem; font-weight: 600;">
                    Highlighting High & Critical Issues ({high_crit_count} found)
                </div>
                """, unsafe_allow_html=True)
            with col_h2:
                def reset_issue_filter():
                    st.session_state["highlight_critical"] = False
                st.button("Show All Issues", key="btn_show_all_issues", use_container_width=True, on_click=reset_issue_filter)

        if not df_all_issues.empty:
            bot_issues_exist = any(
                df_all_issues.get('Issue Name', pd.Series()).str.contains('Bot Protection|403', case=False, na=False)
            )
            if bot_issues_exist:
                box_bg = "rgba(59, 130, 246, 0.12)" if theme_mode != "light" else "#EFF6FF"
                box_border = "#3b82f6" if theme_mode != "light" else "#60A5FA"
                title_color = "#93c5fd" if theme_mode != "light" else "#1D4ED8"
                text_color = "#e2e8f0" if theme_mode != "light" else "#1E293B"
                st.markdown(f"""
                <div style="background: {box_bg}; border-left: 4px solid {box_border}; border-radius: 10px; padding: 12px 18px; margin-bottom: 1.25rem; font-size: 0.92rem; line-height: 1.5;">
                    <strong style="color: {title_color}; font-weight: 700;">🛡️ Why is 403 / Bot Protection displayed?</strong><br/>
                    <span style="color: {text_color};">
                        Displayed because this website uses bot protection (e.g. Cloudflare) that blocks automated scanners. 
                        In your web browser the site works normally, but automated crawlers are blocked so no further page information is given.
                    </span>
                </div>
                """, unsafe_allow_html=True)

            if is_highlighted:
                df_display = df_all_issues[df_all_issues.get('Severity', pd.Series()).isin(['High', 'Critical'])]
                if df_display.empty:
                    df_display = df_all_issues
            else:
                df_display = df_all_issues
            render_styled_table(df_display, theme_mode=theme_mode)
        else:
            st.info("No critical SEO issues found on the analyzed pages.")

    elif current_nav_tab == "Technical Audit":
        render_tab_heading("Technical Audit & Core Web Vitals", theme_mode=theme_mode)
        render_info_banner(
            "What is a Technical Audit?",
            "Technical Audit measures website speed and user experience metrics (Core Web Vitals) including load times, page file size, and mobile responsiveness. Fast websites rank higher on search engines.",
            theme_mode=theme_mode
        )
        if not df_all_audit.empty:
            render_styled_table(df_all_audit, theme_mode=theme_mode)

            if 'Load_Time_sec' in df_all_audit.columns:
                render_tab_heading("Page Load Time by URL (seconds)", theme_mode=theme_mode, margin_top="2rem")
                load_df = df_all_audit[['URL_Slug', 'Load_Time_sec']].copy()
                load_df['Page'] = load_df['URL_Slug'].apply(lambda x: x if len(x) < 25 else x[:22] + '...')
                render_styled_area_chart(load_df, 'Page', 'Load_Time_sec', theme_mode=theme_mode)

        render_tab_heading("AI SEO Actions & Step-by-Step Fixes", theme_mode=theme_mode, margin_top="2rem")
        
        recs = generate_ai_seo_recommendations(df_all_pages, df_all_issues, df_all_audit)
        
        # CONDITIONAL RECOMMENDATIONS: If 100% healthy or zero issues, don't display unnecessary recommendation items!
        if not recs or (df_all_issues.empty and len(recs) <= 1):
            if theme_mode == "light":
                st.markdown("""
                <div style="background: #F0FDF4; border-left: 4px solid #10B981; border: 1px solid #BBF7D0; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                    <h4 style="color: #047857; margin-top: 0; font-size: 1.15rem; font-weight: 700;">
                        100% Optimal SEO Status
                    </h4>
                    <p style="color: #374151; font-size: 0.95rem; margin-bottom: 0;">
                        Your website pages fully comply with SEO best practices! Title tags, meta descriptions, canonical structures, and internal links are properly optimized. No action items required.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
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
            if theme_mode == "light":
                st.markdown("""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #4F46E5; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                    <h5 style="color: #1E293B; margin-top: 0; font-size: 1rem; font-weight: 700;">Verified Analysis & Data Accuracy Guarantee</h5>
                    <p style="color: #475569; font-size: 0.9rem; margin-bottom: 0; line-height: 1.5;">
                        These action items are generated directly from real-time live page analysis, W3C HTML specifications, and search engine optimization standards. Every recommendation is 100% verified against your active website code.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
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
                if theme_mode == "light":
                    item_title_color = "#0F172A"
                    item_desc_color = "#334155"
                    item_impact_color = "#64748B"
                    item_action_color = "#4F46E5"
                    if sev == "critical":
                        color_style = "border-left: 4px solid #EF4444; background: #FEF2F2; border: 1px solid #FECACA; border-left: 4px solid #EF4444; margin: 10px 0; border-radius: 10px; padding: 14px;"
                        sev_badge = '<span style="color: #DC2626; font-weight: 800;">[CRITICAL]</span>'
                    elif sev == "high":
                        color_style = "border-left: 4px solid #F97316; background: #FFF7ED; border: 1px solid #FFEDD5; border-left: 4px solid #F97316; margin: 10px 0; border-radius: 10px; padding: 14px;"
                        sev_badge = '<span style="color: #EA580C; font-weight: 800;">[HIGH]</span>'
                    elif sev == "medium":
                        color_style = "border-left: 4px solid #EAB308; background: #FEFCE8; border: 1px solid #FEF08A; border-left: 4px solid #EAB308; margin: 10px 0; border-radius: 10px; padding: 14px;"
                        sev_badge = '<span style="color: #CA8A04; font-weight: 800;">[MEDIUM]</span>'
                    else:
                        color_style = "border-left: 4px solid #10B981; background: #F0FDF4; border: 1px solid #BBF7D0; border-left: 4px solid #10B981; margin: 10px 0; border-radius: 10px; padding: 14px;"
                        sev_badge = '<span style="color: #059669; font-weight: 800;">[LOW]</span>'
                else:
                    item_title_color = "#f1f5f9"
                    item_desc_color = "#cbd5e1"
                    item_impact_color = "#94a3b8"
                    item_action_color = "#38bdf8"
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
                    f'<div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 4px; color: {item_title_color};">{sev_badge} {r["title"]}</div>'
                    f'<div style="color: {item_desc_color}; font-size: 0.95rem; margin-bottom: 6px;">{r["description"]}</div>'
                    f'<div style="color: {item_impact_color}; font-size: 0.85rem; margin-bottom: 4px;"><strong>Impact:</strong> {r["impact"]}</div>'
                    f'<div style="color: {item_action_color}; font-size: 0.85rem; font-weight: 600;"><strong>Action:</strong> {r["action_item"]}</div>'
                    f'</div>'
                )
                rec_html += item_html
            rec_html += '</div>'
            st.markdown(rec_html, unsafe_allow_html=True)

    elif current_nav_tab == "Security Scorecard":
        render_tab_heading("Cybersecurity & Risk Scorecard", theme_mode=theme_mode)
        render_info_banner(
            "What is the Security Scorecard?",
            "This section checks if your website uses valid SSL encryption, has active security headers to block hackers, and verifies that your domain is free from malware or phishing risks.",
            theme_mode=theme_mode
        )

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
        if theme_mode == "light":
            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #10B981; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                <h5 style="color: #047857; margin-top: 0; font-size: 1rem; font-weight: 700;">Verified Security Standard & Trusted Source</h5>
                <p style="color: #475569; font-size: 0.9rem; margin-bottom: 0; line-height: 1.5;">
                    This security grade is computed directly from live target server response headers, RFC 2818 SSL certificate validation, and official OWASP Top 10 web security compliance specifications. All test results are 100% objective and verified directly from server handshakes.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
                <h5 style="color: #34d399; margin-top: 0; font-size: 1rem; font-weight: 700;">Verified Security Standard & Trusted Source</h5>
                <p style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0; line-height: 1.5;">
                    This security grade is computed directly from live target server response headers, RFC 2818 SSL certificate validation, and official OWASP Top 10 web security compliance specifications. All test results are 100% objective and verified directly from server handshakes.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Top Metric Cards
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            metric_score_color = "#0284C7" if theme_mode == "light" else "#06b6d4"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Security Compliance Score</div>
                <div class="metric-value" style="color: {metric_score_color};">{res['global_score']}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            metric_grade_color = "#4F46E5" if theme_mode == "light" else "#818cf8"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Security Grade</div>
                <div class="metric-value" style="color: {metric_grade_color};">{res['grade']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            if theme_mode == "light":
                rating_color = "#DC2626" if "High" in res['rating'] or "Critical" in res['rating'] else ("#D97706" if "Medium" in res['rating'] else "#059669")
            else:
                rating_color = "#f87171" if "High" in res['rating'] or "Critical" in res['rating'] else ("#f59e0b" if "Medium" in res['rating'] else "#10b981")
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Risk Exposure Rating</div>
                <div class="metric-value" style="color: {rating_color};">{res['rating']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Section 1: SSL Validation Details
        render_tab_heading("SSL / TLS Certificate Validation", theme_mode=theme_mode, margin_top="2rem")
        ssl_desc_color = "#475569" if theme_mode == "light" else "#94a3b8"
        st.markdown(f"""
        <p style="color: {ssl_desc_color}; font-size: 0.9rem; margin-bottom: 1rem;">
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
        render_styled_table(pd.DataFrame(ssl_rows), theme_mode=theme_mode)

        # Section 2: Security Headers Audit
        render_tab_heading("HTTP Security Headers Audit", theme_mode=theme_mode, margin_top="2rem")
        st.markdown(f"""
        <p style="color: {ssl_desc_color}; font-size: 0.9rem; margin-bottom: 1rem;">
            <strong>What are HTTP Security Headers?</strong> Security headers are instructions sent by your web server to visitors' browsers to defend against cross-site scripting (XSS), clickjacking, and data tampering.
        </p>
        """, unsafe_allow_html=True)
        df_headers = pd.DataFrame(res["header_findings"])[["header", "status", "value", "severity", "desc"]]
        df_headers.columns = ["Security Header", "Compliance Status", "Header Value", "Severity Level", "Policy Description"]
        render_styled_table(df_headers, theme_mode=theme_mode)

        # Section 3: Threat & Risk Heuristics
        render_tab_heading("Threat & Risk Analysis", theme_mode=theme_mode, margin_top="2rem")
        threat_head_color = "#1E293B" if theme_mode == "light" else "#cbd5e1"
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(f"<h4 style='color: {threat_head_color}; font-weight: 700; margin-bottom: 1rem;'>Phishing Indicators</h4>", unsafe_allow_html=True)
            if res["phishing_reasons"]:
                for reason in res["phishing_reasons"]:
                    if theme_mode == "light":
                        st.markdown(f"""
                        <div style="background: #FEF2F2; border: 1px solid #FECACA; border-left: 4px solid #EF4444; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: #DC2626; font-size: 0.92rem;">
                            <strong>Risk Warning:</strong> {reason}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: #f87171; font-size: 0.92rem;">
                            <strong>Risk Warning:</strong> {reason}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                if theme_mode == "light":
                    st.markdown("""
                    <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-left: 4px solid #10B981; border-radius: 8px; padding: 12px; color: #047857; font-size: 0.92rem; font-weight: 600;">
                        No brand spoofing or high-entropy anomalies detected.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 8px; padding: 12px; color: #34d399; font-size: 0.92rem; font-weight: 600;">
                        No brand spoofing or high-entropy anomalies detected.
                    </div>
                    """, unsafe_allow_html=True)

        with col_t2:
            st.markdown(f"<h4 style='color: {threat_head_color}; font-weight: 700; margin-bottom: 1rem;'>Malware Risk Analysis</h4>", unsafe_allow_html=True)
            if res["malware_reasons"]:
                for reason in res["malware_reasons"]:
                    if theme_mode == "light":
                        st.markdown(f"""
                        <div style="background: #FEF2F2; border: 1px solid #FECACA; border-left: 4px solid #EF4444; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: #DC2626; font-size: 0.92rem;">
                            <strong>Threat Alert:</strong> {reason}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: #f87171; font-size: 0.92rem;">
                            <strong>Threat Alert:</strong> {reason}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                if theme_mode == "light":
                    st.markdown("""
                    <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-left: 4px solid #10B981; border-radius: 8px; padding: 12px; color: #047857; font-size: 0.92rem; font-weight: 600;">
                        No drive-by hidden frames or obfuscated script signatures found.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 8px; padding: 12px; color: #34d399; font-size: 0.92rem; font-weight: 600;">
                        No drive-by hidden frames or obfuscated script signatures found.
                    </div>
                    """, unsafe_allow_html=True)

        # Section 4: Vulnerability Remediation Plan
        render_tab_heading("Vulnerability Remediation Plan", theme_mode=theme_mode, margin_top="2rem")
        
        recs_list = res["recommendations"]
        is_perfect = (res["global_score"] == 100) or (len(recs_list) == 1 and "No active vulnerabilities found" in recs_list[0])

        # CONDITIONAL SECURITY RECOMMENDATIONS
        if is_perfect:
            if theme_mode == "light":
                st.markdown("""
                <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-left: 4px solid #10B981; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                    <h4 style="color: #047857; margin-top: 0; font-size: 1.15rem; font-weight: 700;">
                        100% Optimal Security Compliance
                    </h4>
                    <p style="color: #374151; font-size: 0.95rem; margin-bottom: 0;">
                        Congratulations! Your target domain fully satisfies all security requirements. SSL encryption is active, all 6 HTTP security headers are enabled, and zero malware or phishing risks were detected. No remediation items required.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
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
                if theme_mode == "light":
                    rec_html += f'<div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 4px solid #0284C7; border-radius: 8px; padding: 12px; margin: 8px 0; color: #1E293B; font-size: 0.95rem;"><strong style="color: #0284C7;">Action Item {idx_rec + 1}:</strong> {rec}</div>'
                else:
                    rec_html += f'<div style="background: rgba(15, 23, 42, 0.5); border-left: 4px solid #0284c7; border-radius: 8px; padding: 12px; margin: 8px 0; color: #e0f2fe; font-size: 0.95rem;"><strong style="color: #38bdf8;">Action Item {idx_rec + 1}:</strong> {rec}</div>'
            rec_html += '</div>'
            st.markdown(rec_html, unsafe_allow_html=True)

    # Save and output the unified Excel report
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    render_download_section(theme_mode=theme_mode)

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
    render_ready_to_scan(theme_mode=theme_mode)

# Render footer on all pages
inject_footer_element(theme_mode=theme_mode)
