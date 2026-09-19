import streamlit as st

def inject_premium_styles(theme_mode="dark"):
    is_dark = (theme_mode == "dark")

    if is_dark:
        theme_css = """
        /* ================= DARK THEME STYLES ================= */
        .stApp {
            background: radial-gradient(at 0% 0%, rgba(34, 211, 238, 0.12) 0px, transparent 45%),
                        radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 45%),
                        radial-gradient(at 50% 100%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
                        radial-gradient(circle at 50% 0%, #0c1220 0%, #060911 100%) !important;
            color: #f1f5f9 !important;
        }

        h1 {
            background: linear-gradient(135deg, #f8fafc 0%, #38bdf8 50%, #818cf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }
        h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
        h3, h4 { color: #22d3ee !important; font-weight: 700 !important; }
        h5, h6 { color: #f1f5f9 !important; }
        label, p, li { color: #cbd5e1 !important; }

        /* Glassmorphic layout card styling */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.09) !important;
            border-radius: 18px !important;
            padding: 1.8rem !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.04) inset !important;
            margin-bottom: 1.5rem !important;
        }

        /* Actionable recommendations lists */
        .recommendation-item {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.55) 0%, rgba(15, 23, 42, 0.6) 100%) !important;
            border-left: 4px solid #38bdf8 !important;
            border-radius: 10px !important;
            padding: 1rem 1.25rem !important;
            margin: 0.75rem 0 !important;
            color: #cbd5e1 !important;
            font-size: 0.95rem !important;
            border-top: 1px solid rgba(255, 255, 255, 0.04) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
        }

        /* Custom stats metrics */
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.85) 100%) !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 18px !important;
            padding: 1.6rem !important;
            text-align: center !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.05) inset !important;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, box-shadow 0.3s ease !important;
        }
        .metric-card:hover {
            transform: translateY(-4px) !important;
            border-color: rgba(34, 211, 238, 0.6) !important;
            box-shadow: 0 16px 36px rgba(34, 211, 238, 0.2), 0 0 0 1px rgba(34, 211, 238, 0.3) inset !important;
        }
        .metric-label {
            font-size: 0.85rem !important;
            color: #94a3b8 !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            margin-bottom: 0.5rem !important;
        }
        .metric-value {
            font-size: 2.35rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.3) !important;
        }
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
            background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #6366f1 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 28px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 25px rgba(59, 130, 246, 0.35) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            letter-spacing: 0.5px !important;
        }
        div.stButton > button p,
        div.stButton > button span,
        div.stButton > button div {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 700 !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(59, 130, 246, 0.5) !important;
            filter: brightness(1.08) !important;
            color: #ffffff !important;
        }

        /* Theme toggle button specific styling */
        div.st-key-theme_toggle_btn,
        div[class*="st-key-theme_toggle_btn"] {
            display: flex !important;
            justify-content: center !important;
            margin-bottom: 1.25rem !important;
        }
        div.st-key-theme_toggle_btn button,
        div[class*="st-key-theme_toggle_btn"] button {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.6) !important;
            border-radius: 9999px !important;
            color: #38bdf8 !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            padding: 10px 24px !important;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5), 0 0 12px rgba(56, 189, 248, 0.25) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            max-width: 400px !important;
            margin: 0 auto !important;
            min-height: 46px !important;
        }
        div.st-key-theme_toggle_btn button p,
        div.st-key-theme_toggle_btn button span,
        div.st-key-theme_toggle_btn button div {
            color: #38bdf8 !important;
            -webkit-text-fill-color: #38bdf8 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.3px !important;
        }
        div.st-key-theme_toggle_btn button:hover {
            background: rgba(56, 189, 248, 0.2) !important;
            border-color: #38bdf8 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(56, 189, 248, 0.45) !important;
        }
        div.st-key-theme_toggle_btn button:hover p,
        div.st-key-theme_toggle_btn button:hover span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }

        /* Clear Scan / Secondary Buttons */
        div.st-key-clear_scan_btn button,
        div[class*="st-key-clear_scan_btn"] button,
        button[data-testid="stBaseButton-secondary"]:not(.st-key-theme_toggle_btn button) {
            background: rgba(30, 41, 59, 0.75) !important;
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            color: #f87171 !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
        }
        div.st-key-clear_scan_btn button p,
        div.st-key-clear_scan_btn button span {
            color: #f87171 !important;
            -webkit-text-fill-color: #f87171 !important;
        }
        div.st-key-clear_scan_btn button:hover {
            background: rgba(239, 68, 68, 0.15) !important;
            border-color: #ef4444 !important;
            transform: translateY(-1px) !important;
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
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            white-space: nowrap !important;
            min-width: 0 !important;
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
        /* ================= AURORA LIGHT GRADIENT THEME ================= */
        .stApp {
            background: radial-gradient(at 10% 10%, rgba(99, 102, 241, 0.08) 0px, transparent 45%),
                        radial-gradient(at 90% 15%, rgba(6, 182, 212, 0.1) 0px, transparent 50%),
                        radial-gradient(at 50% 85%, rgba(168, 85, 247, 0.07) 0px, transparent 55%),
                        linear-gradient(145deg, #f8fafc 0%, #f1f5f9 40%, #eef2ff 100%) !important;
            color: #0f172a !important;
        }

        h1 {
            background: linear-gradient(135deg, #0f172a 0%, #2563eb 50%, #4f46e5 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }
        h2 { color: #0f172a !important; font-weight: 700 !important; }
        h3, h4 { color: #1d4ed8 !important; font-weight: 700 !important; }
        h5, h6 { color: #0f172a !important; }
        label, p, li { color: #475569 !important; }

        /* Crisp glassmorphic card styling with multi-layer shadow */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(226, 232, 240, 0.85) !important;
            border-radius: 18px !important;
            padding: 1.8rem !important;
            box-shadow: 0 10px 30px -5px rgba(99, 102, 241, 0.06), 0 4px 6px -2px rgba(0, 0, 0, 0.02), 0 0 0 1px rgba(255, 255, 255, 0.9) inset !important;
            margin-bottom: 1.5rem !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }

        /* Actionable recommendations lists */
        .recommendation-item {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
            border-left: 4px solid #4f46e5 !important;
            border-radius: 10px !important;
            padding: 1rem 1.25rem !important;
            margin: 0.75rem 0 !important;
            color: #1e293b !important;
            font-size: 0.95rem !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
            border-top: 1px solid rgba(241, 245, 249, 0.8) !important;
            border-right: 1px solid rgba(241, 245, 249, 0.8) !important;
            border-bottom: 1px solid rgba(241, 245, 249, 0.8) !important;
        }

        /* Custom stats metrics */
        .metric-card {
            background: linear-gradient(140deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 245, 255, 0.85) 100%) !important;
            border: 1px solid rgba(199, 210, 254, 0.7) !important;
            border-radius: 18px !important;
            padding: 1.6rem !important;
            text-align: center !important;
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.8) inset !important;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease, border-color 0.3s ease !important;
        }
        .metric-card:hover {
            transform: translateY(-4px) !important;
            border-color: #4f46e5 !important;
            box-shadow: 0 16px 32px -4px rgba(79, 70, 229, 0.18), 0 0 0 1px rgba(255, 255, 255, 0.9) inset !important;
        }
        .metric-label {
            font-size: 0.85rem !important;
            color: #475569 !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            margin-bottom: 0.5rem !important;
        }
        .metric-value {
            font-size: 2.35rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #1d4ed8 0%, #4f46e5 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
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
            color: #ffffff !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 28px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.35) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            letter-spacing: 0.5px !important;
        }
        div.stButton > button p,
        div.stButton > button span,
        div.stButton > button div {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 700 !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5) !important;
            filter: brightness(1.05) !important;
            color: #ffffff !important;
        }

        /* Theme toggle button specific styling in Light Mode */
        div.st-key-theme_toggle_btn,
        div[class*="st-key-theme_toggle_btn"] {
            display: flex !important;
            justify-content: center !important;
            margin-bottom: 1.25rem !important;
        }
        div.st-key-theme_toggle_btn button,
        div[class*="st-key-theme_toggle_btn"] button {
            background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%) !important;
            border: 1.5px solid #3b82f6 !important;
            border-radius: 9999px !important;
            color: #1d4ed8 !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            padding: 10px 24px !important;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.18), 0 0 0 1px rgba(255, 255, 255, 0.9) inset !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            max-width: 400px !important;
            margin: 0 auto !important;
            min-height: 46px !important;
        }
        div.st-key-theme_toggle_btn button p,
        div.st-key-theme_toggle_btn button span,
        div.st-key-theme_toggle_btn button div {
            color: #1d4ed8 !important;
            -webkit-text-fill-color: #1d4ed8 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.3px !important;
        }
        div.st-key-theme_toggle_btn button:hover {
            background: #dbeafe !important;
            border-color: #1d4ed8 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
        }
        div.st-key-theme_toggle_btn button:hover p,
        div.st-key-theme_toggle_btn button:hover span {
            color: #1e40af !important;
            -webkit-text-fill-color: #1e40af !important;
        }

        /* Clear Scan / Secondary Buttons in Light Mode */
        div.st-key-clear_scan_btn button,
        div[class*="st-key-clear_scan_btn"] button,
        button[data-testid="stBaseButton-secondary"]:not(.st-key-theme_toggle_btn button) {
            background: #ffffff !important;
            border: 1px solid #fca5a5 !important;
            color: #dc2626 !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 2px 8px rgba(220, 38, 38, 0.08) !important;
        }
        div.st-key-clear_scan_btn button p,
        div.st-key-clear_scan_btn button span {
            color: #dc2626 !important;
            -webkit-text-fill-color: #dc2626 !important;
        }
        div.st-key-clear_scan_btn button:hover {
            background: #fef2f2 !important;
            border-color: #ef4444 !important;
            transform: translateY(-1px) !important;
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
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            white-space: nowrap !important;
            min-width: 0 !important;
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

    base_css = """
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        /* Scoped global typography */
        html, body, .stApp, p, label, button, input, select, textarea, h1, h2, h3, h4, h5, h6,
        .glass-card, .metric-card, .recommendation-item, .browser-frame, .info-box {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Preserve Material Symbols & Streamlit Icon Fonts */
        [class*="material-symbols"],
        [class*="material-icons"],
        [class*="icon"],
        [data-testid="stIcon"],
        .material-symbols-outlined,
        .material-symbols-rounded,
        .material-symbols-sharp {
            font-family: 'Material Symbols Outlined', 'Material Icons', 'StreamlitIcons', sans-serif !important;
            font-style: normal !important;
            text-transform: none !important;
        }

        footer {visibility: hidden;}

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        .block-container {
            padding-top: 3.5rem !important;
            padding-bottom: 4rem !important;
            max-width: 1200px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        /* App Title & Subtitle Typography */
        .main-app-title {
            font-size: 2.85rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
            margin-bottom: 0.5rem !important;
            line-height: 1.15 !important;
            text-align: center !important;
        }
        .main-app-title.gradient-title-dark {
            background: linear-gradient(135deg, #22d3ee 0%, #38bdf8 40%, #818cf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }
        .main-app-title.gradient-title-light {
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #4f46e5 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }
        .main-app-subtitle {
            font-size: 1.1rem !important;
            margin-bottom: 1.25rem !important;
            line-height: 1.5 !important;
            text-align: center !important;
        }

        div[data-baseweb="tab-highlight"] {
            display: none !important;
        }

        /* Keyframe Animations */
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }

        /* Circular spinner */
        .circular-spinner {
            width: 32px;
            height: 32px;
            border: 3px solid rgba(34, 211, 238, 0.2);
            border-radius: 50%;
            border-top: 3px solid #22d3ee;
            animation: spin 1s linear infinite;
            display: inline-block;
        }

        .browser-dot {
            width: 9px !important;
            height: 9px !important;
            border-radius: 50% !important;
            display: inline-block !important;
        }
        .browser-dot.red { background: #ef4444 !important; }
        .browser-dot.yellow { background: #f59e0b !important; }
        .browser-dot.green { background: #10b981 !important; }

        /* ================= MOBILE & TABLET RESPONSIVE SYSTEM ================= */
        @media (max-width: 768px) {
            .block-container {
                padding-top: 2.5rem !important;
                padding-left: 0.85rem !important;
                padding-right: 0.85rem !important;
                padding-bottom: 2.5rem !important;
            }
            .main-app-title {
                font-size: 1.95rem !important;
                letter-spacing: -0.3px !important;
                line-height: 1.2 !important;
            }
            .main-app-subtitle {
                font-size: 0.95rem !important;
                line-height: 1.45 !important;
                padding: 0 0.5rem !important;
                margin-bottom: 1rem !important;
            }
            .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
                padding: 1.2rem 1rem !important;
                border-radius: 14px !important;
                margin-bottom: 1rem !important;
            }
            .metric-card {
                padding: 1rem 0.85rem !important;
                border-radius: 14px !important;
                margin-bottom: 0.75rem !important;
            }
            .metric-value {
                font-size: 1.75rem !important;
            }
            .metric-label {
                font-size: 0.75rem !important;
                letter-spacing: 0.8px !important;
            }
            div.stButton > button {
                padding: 12px 18px !important;
                font-size: 1rem !important;
                min-height: 46px !important;
            }
            div.st-key-theme_toggle_btn button,
            div[class*="st-key-theme_toggle_btn"] button {
                max-width: 100% !important;
                width: 100% !important;
                font-size: 0.88rem !important;
                padding: 10px 16px !important;
            }
            div[data-baseweb="tab-list"] {
                overflow-x: auto !important;
                flex-wrap: nowrap !important;
                white-space: nowrap !important;
                padding-bottom: 4px !important;
            }
            div[data-baseweb="tab"] {
                padding: 8px 12px !important;
                font-size: 0.85rem !important;
            }
            div[data-testid="stDataFrame"] {
                max-width: 100% !important;
                overflow-x: auto !important;
            }
            .browser-frame {
                border-radius: 12px !important;
                margin: 1rem 0 !important;
            }
            .browser-header {
                padding: 6px 10px !important;
                gap: 4px !important;
            }
            .browser-address {
                font-size: 0.72rem !important;
                padding: 2px 8px !important;
                margin-left: 6px !important;
                max-width: 60% !important;
            }
            .recommendation-item {
                padding: 0.85rem 1rem !important;
                font-size: 0.88rem !important;
            }
            textarea, input, select {
                font-size: 16px !important;
            }
        }

        @media (max-width: 480px) {
            .block-container {
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
            }
            .main-app-title {
                font-size: 1.65rem !important;
            }
            .main-app-subtitle {
                font-size: 0.85rem !important;
            }
            .metric-value {
                font-size: 1.55rem !important;
            }
            .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
                padding: 1rem 0.75rem !important;
            }
        }
    """
    st.markdown(f"<style>{base_css}\n{theme_css}</style>", unsafe_allow_html=True)


def inject_header_element(theme_mode="dark"):
    is_dark = (theme_mode == "dark")
    gradient_class = "gradient-title-dark" if is_dark else "gradient-title-light"
    sub_color = "#94a3b8" if is_dark else "#475569"

    st.markdown(f"""
    <div class="main-header-banner" style="text-align: center; margin-bottom: 0.5rem;">
        <h1 class="main-app-title {gradient_class}">
            SEO Domain Intelligence Agent
        </h1>
        <p class="main-app-subtitle" style="color: {sub_color}; font-weight: 500;">
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
