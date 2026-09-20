import streamlit as st

def render_scan_progress(placeholder, domain, current_log, progress_percentage, theme_mode="corporate"):
    """Renders the animated scan progress card — adapts to dark or light theme."""
    display_percent = min(int(progress_percentage), 99)

    if theme_mode == "light":
        card_bg = "linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)"
        card_border = "1px solid #E2E8F0"
        card_shadow = "0 4px 24px rgba(0,0,0,0.08)"
        heading_color = "#1E293B"
        log_color = "#64748B"
        spinner_class = "circular-spinner-light"
        pct_text_color = "#4F46E5"
        bar_bg = "rgba(226, 232, 240, 0.8)"
        bar_gradient = "linear-gradient(90deg, #4F46E5 0%, #0EA5E9 100%)"
        bar_glow = "0 0 12px rgba(79, 70, 229, 0.4)"
    else:  # corporate dark
        card_bg = "linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%)"
        card_border = "1px solid rgba(34, 211, 238, 0.3)"
        card_shadow = "0 10px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(34, 211, 238, 0.15)"
        heading_color = "#22d3ee"
        log_color = "#cbd5e1"
        spinner_class = "circular-spinner"
        pct_text_color = "#22d3ee"
        bar_bg = "rgba(51, 65, 85, 0.5)"
        bar_gradient = "linear-gradient(90deg, #22d3ee 0%, #3b82f6 50%, #6366f1 100%)"
        bar_glow = "0 0 15px rgba(34, 211, 238, 0.6)"

    placeholder.markdown(f"""
    <div style="
        background: {card_bg};
        border: {card_border};
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: {card_shadow};
        margin: 2rem 0;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    ">
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 1.5rem; gap: 1rem;">
            <div class="{spinner_class}"></div>
            <h3 style="color: {heading_color}; font-size: 1.6rem; font-weight: 700; margin: 0;">
                Analyzing {domain}
            </h3>
        </div>
        <div style="color: {log_color}; font-size: 1rem; margin-bottom: 1.5rem; font-weight: 500; height: 24px; animation: pulse 2s infinite;">
            {current_log}
        </div>
        <div style="
            height: 12px;
            background: {bar_bg};
            border-radius: 6px;
            overflow: hidden;
            margin: 1.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
        ">
            <div style="
                height: 100%;
                width: {display_percent}%;
                background: {bar_gradient};
                border-radius: 6px;
                box-shadow: {bar_glow};
                transition: width 0.3s ease-out;
            "></div>
        </div>
        <div style="color: {heading_color}; font-size: 1.1rem; font-weight: 700;">
            Crawl Engine Progress: <span style="color: {pct_text_color};">{display_percent}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_browser_preview(domain, screenshot_url, fallback_url=None, theme_mode="corporate"):
    import re
    clean_host = domain.replace("https://", "").replace("http://", "").rstrip("/").split("/")[0].split(":")[0]
    display_url = domain.replace("https://", "").replace("http://", "").rstrip("/")
    target_link = domain if (domain.startswith("http://") or domain.startswith("https://")) else f"https://{domain}"
    safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', domain)

    if theme_mode == "light":
        container_bg = "#F8FAFC"
        card_title_color = "#4F46E5"
        card_text_color = "#475569"
        btn_bg = "#EEF2FF"
        btn_color = "#4F46E5"
        btn_border = "#C7D2FE"
        loader_spinner = "border: 3px solid rgba(79, 70, 229, 0.15); border-top: 3px solid #4F46E5;"
        loader_text_color = "#4F46E5"
        open_btn_border = "rgba(100,116,139,0.2)"
        open_btn_color = "#64748B"
    else:  # corporate (dark default)
        container_bg = "#0f172a"
        card_title_color = "#38bdf8"
        card_text_color = "#94a3b8"
        btn_bg = "rgba(59, 130, 246, 0.15)"
        btn_color = "#38bdf8"
        btn_border = "rgba(59, 130, 246, 0.4)"
        loader_spinner = "border: 3px solid rgba(34, 211, 238, 0.2); border-top: 3px solid #22d3ee;"
        loader_text_color = "#38bdf8"
        open_btn_border = "rgba(255,255,255,0.1)"
        open_btn_color = card_text_color

    favicon_url = f"https://www.google.com/s2/favicons?domain={clean_host}&sz=32"

    if screenshot_url == "instant":
        st.markdown(f"""
        <div class="browser-frame">
            <div class="browser-header">
                <span class="browser-dot red"></span>
                <span class="browser-dot yellow"></span>
                <span class="browser-dot green"></span>
                <img src="{favicon_url}" style="width: 14px; height: 14px; margin-left: 8px; margin-right: 6px; vertical-align: -2px;" onerror="this.style.display='none';" />
                <span class="browser-address">{display_url}</span>
            </div>
            <div style="width: 100%; min-height: 260px; background: {container_bg}; padding: 3rem 2rem; text-align: center;">
                <h4 style="color: {card_title_color}; margin: 0 0 0.5rem 0; font-size: 1.3rem; font-weight: 700;">Instant Domain Snapshot Active</h4>
                <p style="font-size: 0.95rem; color: {card_text_color}; max-width: 480px; margin: 0 auto 1.5rem auto; line-height: 1.6;">
                    Verified target connection established for <strong>{display_url}</strong>. Real-time DOM and crawler ready for full audit.
                </p>
                <a href="{target_link}" target="_blank" style="display: inline-block; background: {btn_bg}; color: {btn_color}; border: 1px solid {btn_border}; border-radius: 8px; padding: 8px 20px; font-weight: 600; text-decoration: none;">
                    Visit Live Site
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    fb_val = fallback_url if fallback_url else ""
    st.markdown(f"""
    <div class="browser-frame">
        <div class="browser-header">
            <span class="browser-dot red"></span>
            <span class="browser-dot yellow"></span>
            <span class="browser-dot green"></span>
            <img src="{favicon_url}" style="width: 14px; height: 14px; margin-left: 8px; margin-right: 6px; vertical-align: -2px;" onerror="this.style.display='none';" />
            <span class="browser-address">{display_url}</span>
            <a href="{target_link}" target="_blank" style="color: {open_btn_color}; font-size: 0.78rem; text-decoration: none; padding: 2px 8px; border-radius: 4px; border: 1px solid {open_btn_border}; margin-left: 6px; white-space: nowrap;">Open</a>
        </div>
        <div style="width: 100%; min-height: 300px; max-height: 520px; overflow-y: auto; background: {container_bg}; position: relative;">
            <div id="preview-loader-{safe_id}" style="position: absolute; top: 0; left: 0; width: 100%; height: 300px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: {container_bg}; z-index: 1; transition: opacity 0.3s ease;">
                <div style="width: 32px; height: 32px; {loader_spinner} border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 12px;"></div>
                <div style="color: {loader_text_color}; font-size: 0.92rem; font-weight: 600; letter-spacing: 0.3px;">Fast Preview (1-2s)...</div>
            </div>
            <img id="preview-img-{safe_id}" src="{screenshot_url}"
                onload="var l=document.getElementById('preview-loader-{safe_id}');if(l){{l.style.opacity='0';setTimeout(function(){{l.style.display='none';}},200);}}"
                onerror="window.handlePreviewErr_{safe_id}();"
                loading="eager" decoding="async"
                style="width: 100%; height: auto; display: block; min-height: 220px; position: relative; z-index: 2;"
                alt="Visual Preview for {display_url}" />
            <div id="preview-fallback-{safe_id}" style="display: none; padding: 3.5rem 2rem; text-align: center; position: relative; z-index: 3;">
                <h4 style="color: {card_title_color}; margin: 0 0 0.5rem 0; font-size: 1.25rem; font-weight: 700;">Live Connection Established</h4>
                <p style="font-size: 0.95rem; color: {card_text_color}; max-width: 480px; margin: 0 auto 1.5rem auto; line-height: 1.6;">
                    Target website verified for <strong>{display_url}</strong>. Ready for in-depth SEO &amp; security crawl.
                </p>
                <a href="{target_link}" target="_blank" style="display: inline-block; background: {btn_bg}; color: {btn_color}; border: 1px solid {btn_border}; border-radius: 8px; padding: 8px 18px; font-weight: 600; text-decoration: none;">
                    Visit Live Site
                </a>
            </div>
            <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" style="display:none;" onload="
                window.handlePreviewErr_{safe_id} = function() {{
                    var img = document.getElementById('preview-img-{safe_id}');
                    var l = document.getElementById('preview-loader-{safe_id}');
                    var fb = document.getElementById('preview-fallback-{safe_id}');
                    var fbUrl = '{fb_val}';
                    if (img && fbUrl && !img.dataset.tried) {{
                        img.dataset.tried = '1';
                        img.src = fbUrl;
                    }} else {{
                        if (img) img.style.display = 'none';
                        if (l) l.style.display = 'none';
                        if (fb) fb.style.display = 'block';
                    }}
                }};
                setTimeout(function() {{
                    var img = document.getElementById('preview-img-{safe_id}');
                    var l = document.getElementById('preview-loader-{safe_id}');
                    if (l && l.style.display !== 'none') {{
                        if (img && img.complete && img.naturalWidth > 0) {{
                            l.style.display = 'none';
                        }} else {{
                            window.handlePreviewErr_{safe_id}();
                        }}
                    }}
                }}, 2600);
            " />
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_cards(total_domains, total_issues, high_crit_issues, on_domains_click=None, on_issues_click=None, on_critical_click=None, theme_mode="corporate"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button(
            f"TOTAL DOMAINS ANALYZED\n\n{total_domains}",
            key="btn_metric_domains",
            use_container_width=True,
            on_click=on_domains_click
        )

    with col2:
        st.button(
            f"TOTAL SEO ISSUES\n\n{total_issues}",
            key="btn_metric_seo_issues",
            use_container_width=True,
            on_click=on_issues_click
        )

    with col3:
        st.button(
            f"HIGH & CRITICAL ISSUES\n\n{high_crit_issues}",
            key="btn_metric_critical_issues",
            use_container_width=True,
            on_click=on_critical_click,
            args=(high_crit_issues,) if on_critical_click else None
        )


def render_ready_to_scan(theme_mode="corporate"):
    if theme_mode == "light":
        title_color = "#4F46E5"
        desc_color = "#475569"
        bg_color = "#EEF2FF"
        border_color = "#C7D2FE"
        accent_line = "border-left: 4px solid #4F46E5; border-radius: 0 16px 16px 0;"
    else:  # corporate dark
        title_color = "#38bdf8"
        desc_color = "#94a3b8"
        bg_color = "rgba(30, 41, 59, 0.6)"
        border_color = "rgba(59, 130, 246, 0.35)"
        accent_line = "border: 1px dashed rgba(59, 130, 246, 0.35); border-radius: 16px;"

    st.markdown(f"""
    <div style="text-align: center; padding: 3rem 2rem; background: {bg_color}; {accent_line} margin-top: 2rem;">
        <h3 style="color: {title_color}; margin-top: 0; font-weight: 700;">Ready to Run SEO Scan</h3>
        <p style="color: {desc_color}; max-width: 600px; margin: 0 auto; font-size: 1.05rem; line-height: 1.6;">
            Provide one or more website URLs in the configuration card above, adjust your desired crawl limits, and launch the domain intelligence agent to start auditing.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_download_section(theme_mode="corporate"):
    if theme_mode == "light":
        title_color = "#1E293B"
        desc_color = "#475569"
        border_color = "#CBD5E1"
        bg_color = "#F8FAFC"
        card_border = "border: 1px solid #E2E8F0; border-radius: 14px;"
    else:  # corporate dark
        title_color = "#38bdf8"
        desc_color = "#94a3b8"
        border_color = "rgba(59, 130, 246, 0.4)"
        bg_color = "rgba(30, 41, 59, 0.5)"
        card_border = f"border: 1px dashed {border_color}; border-radius: 14px;"

    st.markdown(f"""
    <div style="text-align: center; padding: 1.6rem; background: {bg_color}; {card_border} margin-bottom: 1rem;">
        <h4 style="color: {title_color}; margin-top:0; font-size:1.2rem; font-weight: 700;">Export Crawl Intelligence Datasets</h4>
        <p style="color: {desc_color}; font-size: 0.92rem; margin-bottom: 0;">Download a consolidated Microsoft Excel spreadsheet containing Domain configurations, Crawled Pages, technical details and parsed SEO issues.</p>
    </div>
    """, unsafe_allow_html=True)
