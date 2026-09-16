import streamlit as st

def inject_premium_styles(theme_mode="dark"):
    is_dark = (theme_mode == "dark")

    if is_dark:
        theme_css = """
        /* ================= DARK THEME STYLES ================= */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #0f172a 0%, #080c14 100%) !important;
            color: #f1f5f9 !important;
        }

        h2 { color: #f1f5f9 !important; }
        h3, h4 { color: #22d3ee !important; }
        h5, h6 { color: #f1f5f9 !important; }
        label, p, li { color: #cbd5e1 !important; }

        /* Glassmorphic layout card styling */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(30, 41, 59, 0.5) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            padding: 1.8rem !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            margin-bottom: 1.5rem !important;
        }

        /* Actionable recommendations lists */
        .recommendation-item {
            background: rgba(30, 41, 59, 0.4) !important;
            border-left: 4px solid #475569 !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin: 0.75rem 0 !important;
            color: #cbd5e1 !important;
            font-size: 0.95rem !important;
        }

        /* Custom stats metrics */
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            text-align: center !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
            transition: transform 0.3s ease, border-color 0.3s ease !important;
        }
        .metric-card:hover {
            transform: translateY(-3px) !important;
            border-color: rgba(34, 211, 238, 0.4) !important;
        }
        .metric-label {
            font-size: 0.85rem !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 0.5rem !important;
        }
        .metric-value {
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            text-shadow: 0 0 15px rgba(34, 211, 238, 0.2) !important;
        }

        /* Input textarea container styling */
        div[data-baseweb="textarea"],
        div[data-baseweb="base-input"],
        div[data-testid="stTextAreaRootElement"],
        div[data-testid="stTextArea"] > div {
            background-color: rgba(15, 23, 42, 0.7) !important;
            background: rgba(15, 23, 42, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }
        div[data-baseweb="textarea"]:focus-within,
        div[data-testid="stTextArea"] > div:focus-within {
            border-color: #22d3ee !important;
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.2) !important;
        }
        div[data-testid="stTextArea"] textarea,
        div[data-baseweb="textarea"] textarea,
        textarea {
            color: #f1f5f9 !important;
            background-color: transparent !important;
            -webkit-text-fill-color: #f1f5f9 !important;
            font-size: 0.95rem !important;
        }

        /* Select box styling */
        div[data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] > div {
            background-color: rgba(15, 23, 42, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
        }
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: #f1f5f9 !important;
        }

        /* Tab lists and buttons */
        div[role="tablist"], div[data-baseweb="tab-list"] {
            background-color: rgba(30, 41, 59, 0.4) !important;
            border-radius: 12px !important;
            padding: 6px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            margin-bottom: 1.5rem !important;
        }
        button[role="tab"], button[data-baseweb="tab"], div[data-baseweb="tab"] {
            color: #94a3b8 !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
            border: none !important;
            background: transparent !important;
        }
        button[role="tab"]:hover, button[data-baseweb="tab"]:hover, div[data-baseweb="tab"]:hover {
            color: #22d3ee !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
        }
        button[role="tab"][aria-selected="true"], button[data-baseweb="tab"][aria-selected="true"], div[data-baseweb="tab"][aria-selected="true"] {
            background-color: rgba(34, 211, 238, 0.18) !important;
            color: #22d3ee !important;
            border: 1px solid rgba(34, 211, 238, 0.3) !important;
        }

        /* Explanatory callout boxes */
        .info-box {
            background: rgba(30, 41, 59, 0.4) !important;
            border-left: 4px solid #22d3ee !important;
            padding: 1rem 1.25rem !important;
            border-radius: 8px !important;
            margin-bottom: 1.5rem !important;
            font-size: 0.95rem !important;
            color: #cbd5e1 !important;
            line-height: 1.6 !important;
        }
        .info-box strong {
            color: #22d3ee !important;
        }

        .guarantee-box {
            background: rgba(15, 23, 42, 0.7) !important;
            border: 1px solid rgba(34, 211, 238, 0.3) !important;
            border-radius: 12px !important;
            padding: 1.25rem !important;
            margin-bottom: 1.5rem !important;
        }

        /* Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #22d3ee 0%, #3b82f6 50%, #6366f1 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 28px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 25px rgba(59, 130, 246, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            letter-spacing: 0.5px !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(59, 130, 246, 0.45) !important;
            filter: brightness(1.08) !important;
            color: white !important;
        }

        /* Theme toggle button specific styling */
        button[key="theme_toggle_btn"],
        div[data-testid="stButton"] button[kind="secondary"] {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid rgba(34, 211, 238, 0.4) !important;
            color: #22d3ee !important;
            font-size: 0.95rem !important;
            padding: 8px 16px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
        }
        button[key="theme_toggle_btn"]:hover,
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background: rgba(34, 211, 238, 0.15) !important;
            border-color: #22d3ee !important;
            color: #ffffff !important;
        }

        /* Download button redesign */
        div.stDownloadButton > button {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            letter-spacing: 0.5px !important;
        }
        div.stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(34, 211, 238, 0.25) !important;
            border-color: #22d3ee !important;
            color: white !important;
        }

        /* Browser Mockup Frame Styles */
        .browser-frame {
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 14px !important;
            background: rgba(15, 23, 42, 0.5) !important;
            overflow: hidden !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
        }
        .browser-header {
            background: rgba(30, 41, 59, 0.8) !important;
            padding: 8px 14px !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        .browser-address {
            background: rgba(15, 23, 42, 0.6) !important;
            color: #94a3b8 !important;
            font-size: 0.78rem !important;
            padding: 3px 12px !important;
            border-radius: 6px !important;
            margin-left: 10px !important;
            flex-grow: 1 !important;
            font-family: monospace !important;
        }

        /* Popovers & Tooltips */
        div[data-baseweb="popover"],
        div[data-baseweb="menu"],
        ul[role="listbox"],
        div[role="listbox"],
        div[data-testid="stColumnMenu"],
        div[data-baseweb="tooltip"],
        [data-testid="stPopoverContent"] {
            background-color: #0f172a !important;
            border: 1px solid rgba(34, 211, 238, 0.3) !important;
            border-radius: 12px !important;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6) !important;
            color: #f1f5f9 !important;
            z-index: 999999 !important;
        }
        div[data-baseweb="menu"] li:hover,
        div[role="option"]:hover,
        div[role="option"][aria-selected="true"],
        ul[role="listbox"] li:hover {
            background-color: rgba(34, 211, 238, 0.15) !important;
            color: #22d3ee !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            overflow: auto !important;
        }

        /* Prevent Glide Data Grid sticky/detached overlays on double-click */
        .gdg-bubble,
        [class*="bubble"],
        [class*="gdg-bubble"],
        .dvn-edit-overlay,
        [class*="dvn-edit-overlay"],
        .glideDataGrid-edit-overlay,
        div[data-testid="stDataFrame"] div[class*="portal"],
        div[data-testid="stDataFrame"] div[class*="bubble"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        """
    else:
        theme_css = """
        /* ================= LIGHT / WHITE THEME STYLES ================= */
        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
            color: #0f172a !important;
        }

        h2 { color: #0f172a !important; }
        h3, h4 { color: #1d4ed8 !important; }
        h5, h6 { color: #0f172a !important; }
        label, p, li { color: #475569 !important; }

        /* Crisp white card styling */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 16px !important;
            padding: 1.8rem !important;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.03) !important;
            margin-bottom: 1.5rem !important;
        }

        /* Actionable recommendations lists */
        .recommendation-item {
            background: #f8fafc !important;
            border-left: 4px solid #3b82f6 !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin: 0.75rem 0 !important;
            color: #334155 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }

        /* Custom stats metrics */
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            text-align: center !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
            transition: transform 0.3s ease, border-color 0.3s ease !important;
        }
        .metric-card:hover {
            transform: translateY(-3px) !important;
            border-color: #3b82f6 !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15) !important;
        }
        .metric-label {
            font-size: 0.85rem !important;
            color: #64748b !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 0.5rem !important;
        }
        .metric-value {
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            color: #2563eb !important;
        }

        /* Force high-contrast white styling on BaseWeb textarea containers */
        div[data-baseweb="textarea"],
        div[data-baseweb="base-input"],
        div[data-testid="stTextAreaRootElement"],
        div[data-testid="stTextArea"] > div {
            background-color: #ffffff !important;
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
        }
        div[data-baseweb="textarea"]:focus-within,
        div[data-testid="stTextArea"] > div:focus-within {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
        }
        div[data-testid="stTextArea"] textarea,
        div[data-baseweb="textarea"] textarea,
        textarea {
            color: #0f172a !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
            -webkit-text-fill-color: #0f172a !important;
            font-size: 0.95rem !important;
        }

        /* Select box styling */
        div[data-baseweb="select"],
        div[data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] > div {
            background-color: #ffffff !important;
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
        }
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div,
        div[data-baseweb="select"] svg {
            color: #0f172a !important;
            fill: #0f172a !important;
        }

        /* Tab lists and buttons */
        div[role="tablist"], div[data-baseweb="tab-list"] {
            background-color: #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 6px !important;
            border: 1px solid #cbd5e1 !important;
            margin-bottom: 1.5rem !important;
        }
        button[role="tab"], button[data-baseweb="tab"], div[data-baseweb="tab"] {
            color: #64748b !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
            border: none !important;
            background: transparent !important;
        }
        button[role="tab"]:hover, button[data-baseweb="tab"]:hover, div[data-baseweb="tab"]:hover {
            color: #2563eb !important;
            background-color: rgba(255, 255, 255, 0.6) !important;
        }
        button[role="tab"][aria-selected="true"], button[data-baseweb="tab"][aria-selected="true"], div[data-baseweb="tab"][aria-selected="true"] {
            background-color: #ffffff !important;
            color: #2563eb !important;
            border: 1px solid #cbd5e1 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        }

        /* Explanatory callout boxes */
        .info-box {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-left: 4px solid #2563eb !important;
            padding: 1rem 1.25rem !important;
            border-radius: 8px !important;
            margin-bottom: 1.5rem !important;
            font-size: 0.95rem !important;
            color: #334155 !important;
            line-height: 1.6 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
        }
        .info-box strong {
            color: #1d4ed8 !important;
        }

        .guarantee-box {
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            padding: 1.25rem !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
        }

        /* Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #4f46e5 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 28px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            letter-spacing: 0.5px !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.45) !important;
            filter: brightness(1.05) !important;
            color: white !important;
        }

        /* Theme toggle button specific styling in Light Mode */
        button[key="theme_toggle_btn"],
        div[data-testid="stButton"] button[kind="secondary"] {
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            color: #1d4ed8 !important;
            font-size: 0.95rem !important;
            padding: 8px 16px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        }
        button[key="theme_toggle_btn"]:hover,
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background: #eff6ff !important;
            border-color: #2563eb !important;
            color: #1e40af !important;
        }

        /* Download button redesign */
        div.stDownloadButton > button {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            letter-spacing: 0.5px !important;
        }
        div.stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.15) !important;
            border-color: #2563eb !important;
            color: #2563eb !important;
        }

        /* Browser Mockup Frame Styles */
        .browser-frame {
            border: 1px solid #cbd5e1 !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            overflow: hidden !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06) !important;
        }
        .browser-header {
            background: #f1f5f9 !important;
            padding: 8px 14px !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
            border-bottom: 1px solid #e2e8f0 !important;
        }
        .browser-address {
            background: #ffffff !important;
            color: #475569 !important;
            border: 1px solid #e2e8f0 !important;
            font-size: 0.78rem !important;
            padding: 3px 12px !important;
            border-radius: 6px !important;
            margin-left: 10px !important;
            flex-grow: 1 !important;
            font-family: monospace !important;
        }

        /* Popovers & Tooltips */
        div[data-baseweb="popover"],
        div[data-baseweb="menu"],
        ul[role="listbox"],
        div[role="listbox"],
        div[data-testid="stColumnMenu"],
        div[data-baseweb="tooltip"],
        [data-testid="stPopoverContent"] {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.12) !important;
            color: #0f172a !important;
            z-index: 999999 !important;
        }
        div[data-baseweb="menu"] li:hover,
        div[role="option"]:hover,
        div[role="option"][aria-selected="true"],
        ul[role="listbox"] li:hover {
            background-color: #eff6ff !important;
            color: #2563eb !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            background: #ffffff !important;
            overflow: auto !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        }

        /* Prevent Glide Data Grid sticky/detached overlays on double-click */
        .gdg-bubble,
        [class*="bubble"],
        [class*="gdg-bubble"],
        .dvn-edit-overlay,
        [class*="dvn-edit-overlay"],
        .glideDataGrid-edit-overlay,
        div[data-testid="stDataFrame"] div[class*="portal"],
        div[data-testid="stDataFrame"] div[class*="bubble"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        div[data-testid="stExpander"] {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        }
        """

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        /* Scoped global typography */
        html, body, .stApp, p, label, button, input, select, textarea, h1, h2, h3, h4, h5, h6,
        .glass-card, .metric-card, .recommendation-item, .browser-frame, .info-box {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* Preserve Material Symbols & Streamlit Icon Fonts */
        [class*="material-symbols"],
        [class*="material-icons"],
        [class*="icon"],
        [data-testid="stIcon"],
        .material-symbols-outlined,
        .material-symbols-rounded,
        .material-symbols-sharp {{
            font-family: 'Material Symbols Outlined', 'Material Icons', 'StreamlitIcons', sans-serif !important;
            font-style: normal !important;
            text-transform: none !important;
        }}

        footer {{visibility: hidden;}}

        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 4rem !important;
            max-width: 95% !important;
        }}

        div[data-baseweb="tab-highlight"] {{
            display: none !important;
        }}

        /* Keyframe Animations */
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.6; }}
            50% {{ opacity: 1; }}
        }}

        /* Circular spinner */
        .circular-spinner {{
            width: 32px;
            height: 32px;
            border: 3px solid rgba(34, 211, 238, 0.2);
            border-radius: 50%;
            border-top: 3px solid #22d3ee;
            animation: spin 1s linear infinite;
            display: inline-block;
        }}

        .browser-dot {{
            width: 9px !important;
            height: 9px !important;
            border-radius: 50% !important;
            display: inline-block !important;
        }}
        .browser-dot.red {{ background: #ef4444 !important; }}
        .browser-dot.yellow {{ background: #f59e0b !important; }}
        .browser-dot.green {{ background: #10b981 !important; }}

        /* Theme-specific overrides */
        {theme_css}
    </style>
    """, unsafe_allow_html=True)


def inject_header_element(theme_mode="dark"):
    is_dark = (theme_mode == "dark")
    if is_dark:
        title_style = "font-weight: 800; background: linear-gradient(135deg, #22d3ee 0%, #6366f1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; font-size: 3.2rem; letter-spacing: -0.5px;"
        sub_color = "#94a3b8"
    else:
        title_style = "font-weight: 800; color: #1d4ed8 !important; margin-bottom: 0.5rem; font-size: 3.2rem; letter-spacing: -0.5px;"
        sub_color = "#475569"

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1 style="{title_style}">
            SEO Domain Intelligence Agent
        </h1>
        <p style="color: {sub_color}; font-size: 1.15rem; margin-bottom: 1.5rem; font-weight: 500;">
            Multi-Website Enterprise SEO Analysis — Powered by Screaming Frog + Semrush + WebPageTest
        </p>
    </div>
    """, unsafe_allow_html=True)


def inject_footer_element(theme_mode="dark"):
    is_dark = (theme_mode == "dark")
    border_color = "rgba(255, 255, 255, 0.08)" if is_dark else "#e2e8f0"
    text_color = "#94a3b8" if is_dark else "#64748b"

    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 2rem 0;
        margin-top: 3.5rem;
        border-top: 1px solid {border_color};
        color: {text_color};
        font-size: 0.92rem;
        letter-spacing: 0.5px;
        font-weight: 500;
    ">
        © 2026 Chronflow Made By Patel Rudra J. ,All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)
