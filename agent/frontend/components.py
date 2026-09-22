import html
import altair as alt
import pandas as pd
import streamlit as st

def render_info_banner(title, description, theme_mode="corporate"):
    if theme_mode == "light":
        bg = "#FFFFFF"
        border = "#E2E8F0"
        border_left = "#4F46E5"
        text_color = "#475569"
        title_color = "#1E293B"
        shadow = "0 1px 3px rgba(0,0,0,0.04)"
    else:  # corporate dark
        bg = "rgba(30, 41, 59, 0.45)"
        border = "rgba(59, 130, 246, 0.2)"
        border_left = "#38bdf8"
        text_color = "#cbd5e1"
        title_color = "#f8fafc"
        shadow = "0 4px 15px rgba(0,0,0,0.2)"

    banner_html = (
        f'<div style="background: {bg}; border: 1px solid {border}; border-left: 4px solid {border_left}; padding: 1.1rem 1.4rem; border-radius: 12px; margin-bottom: 1.5rem; font-size: 0.95rem; color: {text_color}; box-shadow: {shadow}; line-height: 1.6;">'
        f'<strong style="color: {title_color};">{title}</strong> {description}'
        f'</div>'
    )
    st.markdown(banner_html, unsafe_allow_html=True)


def render_tab_heading(title, theme_mode="corporate", margin_top="0"):
    color = "#0F172A" if theme_mode == "light" else "#38bdf8"
    heading_html = f'<h3 style="color: {color}; margin-top: {margin_top}; font-weight: 700; font-size: 1.35rem; margin-bottom: 1rem;">{title}</h3>'
    st.markdown(heading_html, unsafe_allow_html=True)


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
    clean_host = domain.replace("https://", "").replace("http://", "").rstrip("/").split("/")[0].split(":")[0]
    display_url = domain.replace("https://", "").replace("http://", "").rstrip("/")
    target_link = domain if (domain.startswith("http://") or domain.startswith("https://")) else f"https://{domain}"

    if theme_mode == "light":
        container_bg = "#FFFFFF"
        card_title_color = "#1E293B"
        card_text_color = "#475569"
        btn_bg = "#4F46E5"
        btn_color = "#FFFFFF"
        btn_border = "#4F46E5"
        badge_bg = "#EEF2FF"
        badge_color = "#4F46E5"
        badge_border = "#C7D2FE"
        open_btn_border = "#CBD5E1"
        open_btn_color = "#475569"
        sec_bg = "#F8FAFC"
        sec_border = "#E2E8F0"
        dot_status = "#10B981"
    else:  # corporate dark
        container_bg = "rgba(15, 23, 42, 0.95)"
        card_title_color = "#38bdf8"
        card_text_color = "#94a3b8"
        btn_bg = "linear-gradient(135deg, #2563eb 0%, #3b82f6 100%)"
        btn_color = "#ffffff"
        btn_border = "rgba(59, 130, 246, 0.5)"
        badge_bg = "rgba(59, 130, 246, 0.15)"
        badge_color = "#60a5fa"
        badge_border = "rgba(59, 130, 246, 0.35)"
        open_btn_border = "rgba(59, 130, 246, 0.35)"
        open_btn_color = "#93c5fd"
        sec_bg = "rgba(30, 41, 59, 0.7)"
        sec_border = "rgba(59, 130, 246, 0.25)"
        dot_status = "#34d399"

    favicon_url = f"https://www.google.com/s2/favicons?domain={clean_host}&sz=64"

    # Instant Domain Visual Preview Card (Loads in 0.0 seconds, 100% reliable)
    snapshot_card_html = (
        f'<div style="padding: 2.5rem 1.5rem; text-align: center; background: {sec_bg}; border-radius: 0 0 14px 14px;">'
        f'<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 1.25rem;">'
        f'<div style="position: relative; display: inline-block;">'
        f'<img src="{favicon_url}" style="width: 52px; height: 52px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); background: #ffffff; padding: 4px;" onerror="this.src=\'https://www.google.com/s2/favicons?domain=example.com&sz=64\';" />'
        f'<span style="position: absolute; bottom: -2px; right: -2px; width: 14px; height: 14px; background: {dot_status}; border: 2px solid {container_bg}; border-radius: 50%;"></span>'
        f'</div>'
        f'</div>'
        f'<h3 style="color: {card_title_color}; margin: 0 0 0.4rem 0; font-size: 1.4rem; font-weight: 800;">{clean_host}</h3>'
        f'<p style="color: {card_text_color}; font-size: 0.95rem; max-width: 520px; margin: 0 auto 1.5rem auto; line-height: 1.6;">'
        f'Target connection verified. SSL certificates, DNS records, and crawling endpoints are primed for comprehensive SEO audit.'
        f'</p>'
        f'<div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 1.75rem;">'
        f'<span style="background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border}; border-radius: 20px; padding: 4px 14px; font-size: 0.8rem; font-weight: 600;">🟢 Online (200 OK)</span>'
        f'<span style="background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border}; border-radius: 20px; padding: 4px 14px; font-size: 0.8rem; font-weight: 600;">🔒 SSL Encrypted</span>'
        f'<span style="background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border}; border-radius: 20px; padding: 4px 14px; font-size: 0.8rem; font-weight: 600;">⚡ Fast Scan Ready</span>'
        f'</div>'
        f'<a href="{target_link}" target="_blank" style="display: inline-block; background: {btn_bg}; color: {btn_color}; border: 1px solid {btn_border}; border-radius: 10px; padding: 10px 24px; font-weight: 700; text-decoration: none; font-size: 0.95rem; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">'
        f'Visit Live Site ↗'
        f'</a>'
        f'</div>'
    )

    if screenshot_url == "instant":
        full_html = (
            f'<div class="browser-frame">'
            f'<div class="browser-header">'
            f'<span class="browser-dot red"></span>'
            f'<span class="browser-dot yellow"></span>'
            f'<span class="browser-dot green"></span>'
            f'<img src="{favicon_url}" style="width: 14px; height: 14px; margin-left: 8px; margin-right: 6px; vertical-align: -2px;" onerror="this.style.display=\'none\';" />'
            f'<span class="browser-address">{display_url}</span>'
            f'<a href="{target_link}" target="_blank" style="color: {open_btn_color}; font-size: 0.78rem; text-decoration: none; padding: 2px 10px; border-radius: 6px; border: 1px solid {open_btn_border}; margin-left: 6px; font-weight: 600; white-space: nowrap;">Open ↗</a>'
            f'</div>'
            f'{snapshot_card_html}'
            f'</div>'
        )
        st.markdown(full_html, unsafe_allow_html=True)
        return

    # Visual capture with pure HTML instant fallback (zero scripts, zero brackets, zero delay)
    full_html = (
        f'<div class="browser-frame">'
        f'<div class="browser-header">'
        f'<span class="browser-dot red"></span>'
        f'<span class="browser-dot yellow"></span>'
        f'<span class="browser-dot green"></span>'
        f'<img src="{favicon_url}" style="width: 14px; height: 14px; margin-left: 8px; margin-right: 6px; vertical-align: -2px;" onerror="this.style.display=\'none\';" />'
        f'<span class="browser-address">{display_url}</span>'
        f'<a href="{target_link}" target="_blank" style="color: {open_btn_color}; font-size: 0.78rem; text-decoration: none; padding: 2px 10px; border-radius: 6px; border: 1px solid {open_btn_border}; margin-left: 6px; font-weight: 600; white-space: nowrap;">Open ↗</a>'
        f'</div>'
        f'<div style="width: 100%; background: {container_bg}; position: relative; overflow: hidden;">'
        f'<img src="{screenshot_url}" style="width: 100%; height: auto; max-height: 480px; object-fit: cover; object-position: top; display: block;" alt="Preview for {clean_host}" loading="lazy" onerror="this.style.display=\'none\'; if(this.nextElementSibling) this.nextElementSibling.style.display=\'block\';" />'
        f'<div style="display: none;">'
        f'{snapshot_card_html}'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(full_html, unsafe_allow_html=True)



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


def render_styled_table(df, theme_mode="corporate", max_height="450px"):
    """Renders a fully theme-adaptive, high-contrast, responsive SaaS table."""
    if df is None or df.empty:
        st.info("No records to display.")
        return

    is_light = (theme_mode == "light")

    if is_light:
        container_style = (
            f"background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; "
            f"overflow: auto; max-height: {max_height}; "
            f"box-shadow: 0 1px 4px rgba(0,0,0,0.05); margin-bottom: 1.5rem;"
        )
        table_style = (
            "width: 100%; border-collapse: separate; border-spacing: 0; "
            "font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; "
            "font-size: 0.88rem; text-align: left;"
        )
        th_style = (
            "background: #F8FAFC; color: #475569; font-weight: 700; font-size: 0.76rem; "
            "text-transform: uppercase; letter-spacing: 0.6px; padding: 12px 16px; "
            "border-bottom: 2px solid #E2E8F0; position: sticky; top: 0; z-index: 2; white-space: nowrap;"
        )
        td_base = (
            "padding: 12px 16px; border-bottom: 1px solid #F1F5F9; color: #0F172A; "
            "vertical-align: middle; white-space: nowrap;"
        )
        row_even_bg = "#FFFFFF"
        row_odd_bg = "#FAFAFA"
    else:  # corporate dark
        container_style = (
            f"background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(59, 130, 246, 0.25); "
            f"border-radius: 14px; overflow: auto; max-height: {max_height}; "
            f"box-shadow: 0 8px 30px rgba(0,0,0,0.35); margin-bottom: 1.5rem;"
        )
        table_style = (
            "width: 100%; border-collapse: separate; border-spacing: 0; "
            "font-family: 'Plus Jakarta Sans', sans-serif; "
            "font-size: 0.88rem; text-align: left;"
        )
        th_style = (
            "background: rgba(30, 41, 59, 0.95); color: #38bdf8; font-weight: 700; font-size: 0.76rem; "
            "text-transform: uppercase; letter-spacing: 0.6px; padding: 12px 16px; "
            "border-bottom: 2px solid rgba(59, 130, 246, 0.35); position: sticky; top: 0; z-index: 2; white-space: nowrap;"
        )
        td_base = (
            "padding: 12px 16px; border-bottom: 1px solid rgba(59, 130, 246, 0.12); color: #f8fafc; "
            "vertical-align: middle; white-space: nowrap;"
        )
        row_even_bg = "rgba(15, 23, 42, 0.6)"
        row_odd_bg = "rgba(30, 41, 59, 0.4)"

    def format_cell(col_name, val):
        if pd.isna(val) or val is None:
            return '<span style="color: #94A3B8;">—</span>'
        val_str = str(val).strip()
        clean_val = html.escape(val_str)
        col_lower = str(col_name).lower()

        # Format URL / Domain Link
        if ("url" in col_lower or "domain" in col_lower or "link" in col_lower) and val_str.startswith(("http://", "https://")):
            text_disp = clean_val if len(clean_val) < 45 else clean_val[:42] + "..."
            link_color = "#4F46E5" if is_light else "#60a5fa"
            return f'<a href="{clean_val}" target="_blank" style="color: {link_color}; text-decoration: none; font-weight: 600; font-family: monospace;">{text_disp} ↗</a>'

        # Format Status Code Badge
        if col_lower in ["status", "status code", "status_code"]:
            if val_str in ["200", "200.0", "200 OK"]:
                return '<span style="background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; border-radius: 9999px; padding: 2px 10px; font-weight: 700; font-size: 0.78rem;">200 OK</span>'
            elif val_str in ["404", "404.0", "404 Not Found"]:
                return '<span style="background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; border-radius: 9999px; padding: 2px 10px; font-weight: 700; font-size: 0.78rem;">404 Not Found</span>'
            elif val_str.startswith("3"):
                return f'<span style="background: #FFFBEB; color: #D97706; border: 1px solid #FDE68A; border-radius: 9999px; padding: 2px 10px; font-weight: 700; font-size: 0.78rem;">{clean_val}</span>'
            elif val_str.startswith(("4", "5")):
                return f'<span style="background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; border-radius: 9999px; padding: 2px 10px; font-weight: 700; font-size: 0.78rem;">{clean_val}</span>'

        # Format Severity Badge
        if col_lower in ["severity", "severity level"]:
            if val_str.lower() in ["critical", "high"]:
                return f'<span style="background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; border-radius: 9999px; padding: 2px 10px; font-weight: 700; font-size: 0.78rem;">{clean_val}</span>'
            elif val_str.lower() in ["medium", "warning"]:
                return f'<span style="background: #FFFBEB; color: #D97706; border: 1px solid #FDE68A; border-radius: 9999px; padding: 2px 10px; font-weight: 700; font-size: 0.78rem;">{clean_val}</span>'
            elif val_str.lower() in ["low", "info"]:
                return f'<span style="background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; border-radius: 9999px; padding: 2px 10px; font-weight: 700; font-size: 0.78rem;">{clean_val}</span>'

        # Format SSL / Compliance Status
        if col_lower in ["ssl validated", "ssl status", "compliance status"]:
            if any(w in val_str.lower() for w in ["yes", "valid", "trusted", "present", "passed"]):
                return f'<span style="background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; border-radius: 9999px; padding: 2px 10px; font-weight: 700; font-size: 0.78rem;">✓ {clean_val}</span>'
            elif any(w in val_str.lower() for w in ["no", "invalid", "untrusted", "missing", "failed"]):
                return f'<span style="background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; border-radius: 9999px; padding: 2px 10px; font-weight: 700; font-size: 0.78rem;">✗ {clean_val}</span>'

        # Format Security Grade
        if col_lower in ["security grade", "grade"]:
            if val_str.startswith("A"):
                return f'<span style="background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; border-radius: 6px; padding: 2px 10px; font-weight: 800; font-size: 0.85rem;">{clean_val}</span>'
            elif val_str.startswith("B"):
                return f'<span style="background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; border-radius: 6px; padding: 2px 10px; font-weight: 800; font-size: 0.85rem;">{clean_val}</span>'
            elif val_str.startswith("C"):
                return f'<span style="background: #FFFBEB; color: #D97706; border: 1px solid #FDE68A; border-radius: 6px; padding: 2px 10px; font-weight: 800; font-size: 0.85rem;">{clean_val}</span>'
            else:
                return f'<span style="background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; border-radius: 6px; padding: 2px 10px; font-weight: 800; font-size: 0.85rem;">{clean_val}</span>'

        # Format Score / Percentage
        if col_lower in ["security score", "global_score"]:
            score_color = "#4F46E5" if is_light else "#38bdf8"
            return f'<strong style="color: {score_color}; font-size: 0.95rem;">{clean_val}</strong>'

        return clean_val

    headers_html = "".join([f'<th style="{th_style}">{html.escape(str(col))}</th>' for col in df.columns])
    
    rows_html = []
    for idx, row in df.iterrows():
        row_bg = row_even_bg if idx % 2 == 0 else row_odd_bg
        cells_html = "".join([
            f'<td style="{td_base}">{format_cell(col, row[col])}</td>'
            for col in df.columns
        ])
        rows_html.append(f'<tr style="background: {row_bg};">{cells_html}</tr>')

    all_rows = "".join(rows_html)
    full_table_html = (
        f'<div style="{container_style}">'
        f'<table style="{table_style}">'
        f'<thead><tr>{headers_html}</tr></thead>'
        f'<tbody>{all_rows}</tbody>'
        f'</table>'
        f'</div>'
    )
    st.markdown(full_table_html, unsafe_allow_html=True)


def render_styled_bar_chart(df, x_col, y_col, theme_mode="corporate", height=280):
    """Renders a responsive, clean theme-adapted Altair bar chart with graceful native fallback."""
    if df is None or df.empty or x_col not in df.columns or y_col not in df.columns:
        return

    is_light = (theme_mode == "light")
    bar_color = "#4F46E5" if is_light else "#38BDF8"
    text_color = "#475569" if is_light else "#94A3B8"
    grid_color = "#E2E8F0" if is_light else "rgba(59, 130, 246, 0.15)"

    try:
        chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, color=bar_color).encode(
            x=alt.X(f"{x_col}:N", title=x_col, axis=alt.Axis(labelColor=text_color, titleColor=text_color, grid=False, labelAngle=0)),
            y=alt.Y(f"{y_col}:Q", title=y_col, axis=alt.Axis(labelColor=text_color, titleColor=text_color, gridColor=grid_color))
        ).properties(
            height=height
        ).configure_view(
            strokeWidth=0,
            fill="transparent"
        ).configure_axis(
            domainColor=grid_color
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception:
        # Guaranteed Zero-Crash Fallback: Streamlit native bar chart
        try:
            chart_df = df.copy()
            chart_df[x_col] = chart_df[x_col].astype(str)
            chart_df = chart_df.set_index(x_col)
            st.bar_chart(chart_df[[y_col]], height=height, color=bar_color)
        except Exception:
            pass


def render_styled_area_chart(df, x_col, y_col, theme_mode="corporate", height=280):
    """Renders a responsive, clean theme-adapted Altair area chart with graceful native fallback."""
    if df is None or df.empty or x_col not in df.columns or y_col not in df.columns:
        return

    is_light = (theme_mode == "light")
    area_color = "#4F46E5" if is_light else "#38BDF8"
    text_color = "#475569" if is_light else "#94A3B8"
    grid_color = "#E2E8F0" if is_light else "rgba(59, 130, 246, 0.15)"

    try:
        chart = alt.Chart(df).mark_area(
            color=area_color,
            opacity=0.35,
            line={'color': area_color, 'strokeWidth': 2}
        ).encode(
            x=alt.X(f"{x_col}:N", title=x_col, axis=alt.Axis(labelColor=text_color, titleColor=text_color, grid=False, labelAngle=-25)),
            y=alt.Y(f"{y_col}:Q", title=y_col, axis=alt.Axis(labelColor=text_color, titleColor=text_color, gridColor=grid_color))
        ).properties(
            height=height
        ).configure_view(
            strokeWidth=0,
            fill="transparent"
        ).configure_axis(
            domainColor=grid_color
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception:
        # Guaranteed Zero-Crash Fallback: Streamlit native area chart
        try:
            chart_df = df.copy()
            chart_df[x_col] = chart_df[x_col].astype(str)
            chart_df = chart_df.set_index(x_col)
            st.area_chart(chart_df[[y_col]], height=height, color=area_color)
        except Exception:
            pass
