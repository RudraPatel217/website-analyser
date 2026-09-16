import streamlit as st

def render_scan_progress(placeholder, domain, current_log, progress_percentage):
    # Cap progress display at 99% while background crawling & auditing finalizes
    display_percent = min(int(progress_percentage), 99)
    placeholder.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(34, 211, 238, 0.15);
        margin: 2rem 0;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    ">
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 1.5rem; gap: 1rem;">
            <div class="circular-spinner"></div>
            <h3 style="color: #22d3ee; font-size: 1.6rem; font-weight: 700; margin: 0; text-shadow: 0 0 10px rgba(34, 211, 238, 0.3);">
                Analyzing {domain}
            </h3>
        </div>
        <div style="color: #cbd5e1; font-size: 1rem; margin-bottom: 1.5rem; font-weight: 500; height: 24px; animation: pulse 2s infinite;">
            {current_log}
        </div>
        <div style="
            height: 12px;
            background: rgba(51, 65, 85, 0.5);
            border-radius: 6px;
            overflow: hidden;
            margin: 1.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
        ">
            <div style="
                height: 100%;
                width: {display_percent}%;
                background: linear-gradient(90deg, #22d3ee 0%, #3b82f6 50%, #6366f1 100%);
                border-radius: 6px;
                box-shadow: 0 0 15px rgba(34, 211, 238, 0.6);
                transition: width 0.3s ease-out;
            "></div>
        </div>
        <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 700;">
            Crawl Engine Progress: <span style="color: #22d3ee;">{display_percent}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_browser_preview(domain, screenshot_url, fallback_url=None, theme_mode="dark"):
    clean_domain = domain.replace("https://", "").replace("http://", "").rstrip("/").split("/")[0]
    target_link = f"https://{clean_domain}"
    is_dark = (theme_mode == "dark")
    
    container_bg = "#0f172a" if is_dark else "#f8fafc"
    card_title_color = "#22d3ee" if is_dark else "#2563eb"
    card_text_color = "#94a3b8" if is_dark else "#64748b"
    btn_bg = "rgba(34, 211, 238, 0.15)" if is_dark else "#eff6ff"
    btn_color = "#22d3ee" if is_dark else "#2563eb"
    btn_border = "rgba(34, 211, 238, 0.4)" if is_dark else "#93c5fd"

    if fallback_url:
        onerror_attr = f'onerror="if(!this.dataset.tried){{this.dataset.tried=\'1\';this.src=\'{fallback_url}\';}}else{{this.style.display=\'none\';var l=document.getElementById(\'preview-loader-{clean_domain}\');if(l)l.style.display=\'none\';var fb=document.getElementById(\'preview-fallback-{clean_domain}\');if(fb)fb.style.display=\'block\';}}"'
    else:
        onerror_attr = f'onerror="this.style.display=\'none\';var l=document.getElementById(\'preview-loader-{clean_domain}\');if(l)l.style.display=\'none\';var fb=document.getElementById(\'preview-fallback-{clean_domain}\');if(fb)fb.style.display=\'block\';"'

    st.markdown(f"""
    <div class="browser-frame">
        <div class="browser-header">
            <span class="browser-dot red"></span>
            <span class="browser-dot yellow"></span>
            <span class="browser-dot green"></span>
            <span class="browser-address">{clean_domain}</span>
        </div>
        <div style="width: 100%; min-height: 380px; max-height: 550px; overflow-y: auto; background: {container_bg}; position: relative;">
            <div id="preview-loader-{clean_domain}" style="position: absolute; top: 0; left: 0; width: 100%; height: 380px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: {container_bg}; z-index: 1;">
                <div style="width: 38px; height: 38px; border: 3px solid rgba(34, 211, 238, 0.2); border-top: 3px solid #22d3ee; border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 12px;"></div>
                <div style="color: {card_title_color}; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.3px;">Capturing Live Visual Preview...</div>
            </div>
            <img src="{screenshot_url}" {onerror_attr} onload="var l=document.getElementById('preview-loader-{clean_domain}');if(l)l.style.display='none';" loading="eager" decoding="async" style="width: 100%; height: auto; display: block; min-height: 250px; position: relative; z-index: 2;" alt="Homepage Preview for {clean_domain}" />
            <div id="preview-fallback-{clean_domain}" style="display: none; padding: 4rem 2rem; text-align: center; position: relative; z-index: 3;">
                <div style="font-size: 3.2rem; margin-bottom: 1rem;">🌐</div>
                <h4 style="color: {card_title_color}; margin: 0 0 0.5rem 0; font-size: 1.25rem; font-weight: 700;">Homepage Snapshot Registered</h4>
                <p style="font-size: 0.95rem; color: {card_text_color}; max-width: 480px; margin: 0 auto 1.5rem auto; line-height: 1.6;">
                    Website structure successfully cataloged for <strong>{clean_domain}</strong>. You can proceed with full SEO & security auditing.
                </p>
                <a href="{target_link}" target="_blank" style="display: inline-block; background: {btn_bg}; color: {btn_color}; border: 1px solid {btn_border}; border-radius: 8px; padding: 8px 18px; font-weight: 600; text-decoration: none;">
                    Visit Live Site ↗
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_cards(total_domains, total_issues, high_crit_issues, theme_mode="dark"):
    is_dark = (theme_mode == "dark")
    c1_color = "#22d3ee" if is_dark else "#0284c7"
    c2_color = "#818cf8" if is_dark else "#4f46e5"
    c3_color = "#f87171" if is_dark else "#dc2626"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Domains Analyzed</div>
            <div class="metric-value" style="color: {c1_color};">{total_domains}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total SEO Issues</div>
            <div class="metric-value" style="color: {c2_color};">{total_issues}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High & Critical Issues</div>
            <div class="metric-value" style="color: {c3_color};">{high_crit_issues}</div>
        </div>
        """, unsafe_allow_html=True)


def render_ready_to_scan(theme_mode="dark"):
    is_dark = (theme_mode == "dark")
    title_color = "#22d3ee" if is_dark else "#2563eb"
    desc_color = "#94a3b8" if is_dark else "#64748b"
    border_color = "rgba(99, 102, 241, 0.25)" if is_dark else "#cbd5e1"

    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 3rem !important; border: 1px dashed {border_color}; margin-top: 2rem;">
        <h3 style="color: {title_color}; margin-top: 0; font-weight: 700;">Ready to Run SEO Scan</h3>
        <p style="color: {desc_color}; max-width: 600px; margin: 0 auto; font-size: 1.05rem; line-height: 1.6;">
            Provide one or more website URLs in the configuration card above, adjust your desired crawl limits, and launch the domain intelligence agent to start auditing.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_download_section(theme_mode="dark"):
    is_dark = (theme_mode == "dark")
    title_color = "#22d3ee" if is_dark else "#2563eb"
    desc_color = "#94a3b8" if is_dark else "#64748b"
    border_color = "rgba(34, 211, 238, 0.4)" if is_dark else "#93c5fd"

    st.markdown(f"""
    <div class="glass-card" style="text-align: center; border: 1px dashed {border_color}; margin-bottom: 1rem;">
        <h4 style="color: {title_color}; margin-top:0; font-size:1.2rem; font-weight: 700;">Export Crawl Intelligence Datasets</h4>
        <p style="color: {desc_color}; font-size: 0.92rem; margin-bottom: 0;">Download a consolidated Microsoft Excel spreadsheet containing Domain configurations, Crawled Pages, technical details and parsed SEO issues.</p>
    </div>
    """, unsafe_allow_html=True)
