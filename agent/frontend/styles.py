import streamlit as st

def inject_premium_styles(theme_mode="corporate"):
    # Enforce pure Dark Mode themes only
    active_mode = "obsidian" if theme_mode == "obsidian" else "corporate"

    # ================= 1. OBSIDIAN DARK MODE (Midnight & Purple) =================
    theme_obsidian_css = """
        /* Obsidian Dark Mode - Midnight Black & Subtle Dark Violet */
        .stApp {
            background: linear-gradient(180deg, #121212 0%, #1e1b4b 100%) !important;
            color: #e2e8f0 !important;
            min-height: 100vh;
        }

        h1 {
            background: linear-gradient(135deg, #f1f5f9 0%, #c084fc 50%, #38bdf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }
        h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
        h3, h4 { color: #c084fc !important; font-weight: 700 !important; }
        h5, h6 { color: #e2e8f0 !important; }
        label, p, li { color: #cbd5e1 !important; }

        /* Glassmorphic layout card styling */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(30, 27, 75, 0.45) !important;
            border: 1px solid rgba(139, 92, 246, 0.25) !important;
            border-radius: 18px !important;
            padding: 1.8rem !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(139, 92, 246, 0.1) inset !important;
            margin-bottom: 1.5rem !important;
        }

        /* Actionable recommendations lists */
        .recommendation-item {
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(18, 18, 18, 0.75) 100%) !important;
            border-left: 4px solid #8b5cf6 !important;
            border-radius: 10px !important;
            padding: 1rem 1.25rem !important;
            margin: 0.75rem 0 !important;
            color: #e2e8f0 !important;
            font-size: 0.95rem !important;
            border-top: 1px solid rgba(139, 92, 246, 0.15) !important;
            border-right: 1px solid rgba(139, 92, 246, 0.15) !important;
            border-bottom: 1px solid rgba(139, 92, 246, 0.15) !important;
        }

        /* Custom stats metrics */
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.75) 0%, rgba(18, 18, 18, 0.85) 100%) !important;
            border: 1px solid rgba(139, 92, 246, 0.35) !important;
            border-radius: 18px !important;
            padding: 1.6rem !important;
            text-align: center !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45) !important;
            transition: transform 0.3s ease, border-color 0.3s ease !important;
        }
        .metric-card:hover {
            transform: translateY(-3px) !important;
            border-color: #a855f7 !important;
            box-shadow: 0 12px 35px rgba(168, 85, 247, 0.25) !important;
        }
        .metric-label {
            font-size: 0.85rem !important;
            color: #a5b4fc !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 0.5rem !important;
        }
        .metric-value {
            font-size: 2.35rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #c084fc 0%, #38bdf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }

        /* Inputs & Textareas */
        div[data-baseweb="textarea"],
        div[data-baseweb="input"],
        div[data-baseweb="select"] > div {
            background-color: rgba(18, 18, 18, 0.95) !important;
            border: 1.5px solid rgba(139, 92, 246, 0.35) !important;
            border-radius: 12px !important;
            color: #e2e8f0 !important;
            transition: all 0.25s ease !important;
        }
        textarea, input {
            color: #e2e8f0 !important;
            -webkit-text-fill-color: #e2e8f0 !important;
        }
        div[data-baseweb="textarea"]:focus-within,
        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.25) !important;
        }

        /* Primary Action Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 50%, #06b6d4 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 28px !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 22px rgba(139, 92, 246, 0.45) !important;
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
            box-shadow: 0 8px 30px rgba(139, 92, 246, 0.6) !important;
            filter: brightness(1.08) !important;
        }

        /* Theme Segmented Buttons */
        div.st-key-theme_btn_obsidian button {
            background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%) !important;
            border: 1.5px solid #c084fc !important;
            box-shadow: 0 4px 16px rgba(139, 92, 246, 0.5) !important;
        }
        div.st-key-theme_btn_obsidian button p,
        div.st-key-theme_btn_obsidian button span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 700 !important;
        }
        div.st-key-theme_btn_corporate button {
            background: rgba(30, 27, 75, 0.5) !important;
            border: 1px solid rgba(139, 92, 246, 0.3) !important;
        }
        div.st-key-theme_btn_corporate button p,
        div.st-key-theme_btn_corporate button span {
            color: #cbd5e1 !important;
            -webkit-text-fill-color: #cbd5e1 !important;
        }

        /* Secondary & Clear Scan Button */
        div.st-key-clear_scan_btn button,
        div[class*="st-key-clear_scan_btn"] button {
            background: rgba(30, 27, 75, 0.75) !important;
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            color: #f87171 !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
        }
        div.st-key-clear_scan_btn button p,
        div.st-key-clear_scan_btn button span {
            color: #f87171 !important;
            -webkit-text-fill-color: #f87171 !important;
        }

        /* Download button */
        div.stDownloadButton > button {
            background: linear-gradient(135deg, #1e1b4b 0%, #121212 100%) !important;
            color: white !important;
            border: 1px solid rgba(139, 92, 246, 0.35) !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        }
        div.stDownloadButton > button:hover {
            border-color: #a855f7 !important;
            box-shadow: 0 8px 25px rgba(168, 85, 247, 0.3) !important;
        }

        /* Browser Mockup Frame */
        .browser-frame {
            border: 1px solid rgba(139, 92, 246, 0.25) !important;
            border-radius: 14px !important;
            background: rgba(18, 18, 18, 0.8) !important;
            overflow: hidden !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
        }
        .browser-header {
            background: rgba(30, 27, 75, 0.85) !important;
            padding: 8px 14px !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
            border-bottom: 1px solid rgba(139, 92, 246, 0.2) !important;
        }
        .browser-address {
            background: rgba(18, 18, 18, 0.7) !important;
            color: #a5b4fc !important;
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

        /* Popovers */
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
            background-color: #181530 !important;
            border: 1px solid rgba(139, 92, 246, 0.4) !important;
            color: #e2e8f0 !important;
        }
        div[data-baseweb="menu"] li:hover, div[role="option"]:hover, div[role="option"][aria-selected="true"] {
            background-color: rgba(139, 92, 246, 0.25) !important;
            color: #ffffff !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(139, 92, 246, 0.25) !important;
            border-radius: 12px !important;
            background: rgba(18, 18, 18, 0.6) !important;
        }
        div[data-testid="stExpander"] {
            background: rgba(30, 27, 75, 0.4) !important;
            border: 1px solid rgba(139, 92, 246, 0.2) !important;
            border-radius: 12px !important;
        }
    """

    # ================= 2. CORPORATE TRUST (Deep Blues & Slate) =================
    theme_corporate_css = """
        /* Corporate Trust - Deep Slate to Navy Blue */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
            color: #f8fafc !important;
            min-height: 100vh;
        }

        h1 {
            background: linear-gradient(135deg, #ffffff 0%, #60a5fa 50%, #818cf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }
        h2 { color: #f8fafc !important; font-weight: 700 !important; }
        h3, h4 { color: #38bdf8 !important; font-weight: 700 !important; }
        h5, h6 { color: #f8fafc !important; }
        label, p, li { color: #cbd5e1 !important; }

        /* Translucent Blue Cards */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(30, 41, 59, 0.75) !important;
            border: 1px solid rgba(59, 130, 246, 0.25) !important;
            border-radius: 18px !important;
            padding: 1.8rem !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.45) !important;
            margin-bottom: 1.5rem !important;
        }

        /* Actionable recommendations lists */
        .recommendation-item {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.85) 100%) !important;
            border-left: 4px solid #3b82f6 !important;
            border-radius: 10px !important;
            padding: 1rem 1.25rem !important;
            margin: 0.75rem 0 !important;
            color: #f8fafc !important;
            font-size: 0.95rem !important;
            border-top: 1px solid rgba(59, 130, 246, 0.15) !important;
            border-right: 1px solid rgba(59, 130, 246, 0.15) !important;
            border-bottom: 1px solid rgba(59, 130, 246, 0.15) !important;
        }

        /* Custom stats metrics */
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
            border: 1px solid rgba(59, 130, 246, 0.35) !important;
            border-radius: 18px !important;
            padding: 1.6rem !important;
            text-align: center !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35) !important;
            transition: transform 0.3s ease, border-color 0.3s ease !important;
        }
        .metric-card:hover {
            transform: translateY(-3px) !important;
            border-color: #3b82f6 !important;
            box-shadow: 0 12px 35px rgba(59, 130, 246, 0.25) !important;
        }
        .metric-label {
            font-size: 0.85rem !important;
            color: #94a3b8 !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 0.5rem !important;
        }
        .metric-value {
            font-size: 2.35rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }

        /* Inputs & Textareas */
        div[data-baseweb="textarea"],
        div[data-baseweb="input"],
        div[data-baseweb="select"] > div {
            background-color: rgba(15, 23, 42, 0.92) !important;
            border: 1.5px solid rgba(59, 130, 246, 0.35) !important;
            border-radius: 12px !important;
            color: #f8fafc !important;
            transition: all 0.25s ease !important;
        }
        textarea, input {
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
        }
        div[data-baseweb="textarea"]:focus-within,
        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
        }

        /* Royal Blue / Indigo Action Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #4f46e5 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 28px !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 22px rgba(37, 99, 235, 0.4) !important;
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
            box-shadow: 0 8px 30px rgba(37, 99, 235, 0.55) !important;
            filter: brightness(1.08) !important;
        }

        /* Theme Segmented Buttons */
        div.st-key-theme_btn_corporate button {
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
            border: 1.5px solid #60a5fa !important;
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.5) !important;
        }
        div.st-key-theme_btn_corporate button p,
        div.st-key-theme_btn_corporate button span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 700 !important;
        }
        div.st-key-theme_btn_obsidian button {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
        }
        div.st-key-theme_btn_obsidian button p,
        div.st-key-theme_btn_obsidian button span {
            color: #cbd5e1 !important;
            -webkit-text-fill-color: #cbd5e1 !important;
        }

        /* Secondary & Clear Scan Button */
        div.st-key-clear_scan_btn button,
        div[class*="st-key-clear_scan_btn"] button {
            background: rgba(30, 41, 59, 0.75) !important;
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            color: #f87171 !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
        }
        div.st-key-clear_scan_btn button p,
        div.st-key-clear_scan_btn button span {
            color: #f87171 !important;
            -webkit-text-fill-color: #f87171 !important;
        }

        /* Download button */
        div.stDownloadButton > button {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            color: white !important;
            border: 1px solid rgba(59, 130, 246, 0.35) !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        }
        div.stDownloadButton > button:hover {
            border-color: #3b82f6 !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3) !important;
        }

        /* Browser Mockup Frame */
        .browser-frame {
            border: 1px solid rgba(59, 130, 246, 0.25) !important;
            border-radius: 14px !important;
            background: rgba(15, 23, 42, 0.8) !important;
            overflow: hidden !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
        }
        .browser-header {
            background: rgba(30, 41, 59, 0.85) !important;
            padding: 8px 14px !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
            border-bottom: 1px solid rgba(59, 130, 246, 0.2) !important;
        }
        .browser-address {
            background: rgba(15, 23, 42, 0.7) !important;
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

        /* Popovers */
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
            background-color: #0f172a !important;
            border: 1px solid rgba(59, 130, 246, 0.4) !important;
            color: #f8fafc !important;
        }
        div[data-baseweb="menu"] li:hover, div[role="option"]:hover, div[role="option"][aria-selected="true"] {
            background-color: rgba(59, 130, 246, 0.25) !important;
            color: #ffffff !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(59, 130, 246, 0.25) !important;
            border-radius: 12px !important;
            background: rgba(15, 23, 42, 0.6) !important;
        }
        div[data-testid="stExpander"] {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(59, 130, 246, 0.2) !important;
            border-radius: 12px !important;
        }
    """

    theme_css = theme_obsidian_css if active_mode == "obsidian" else theme_corporate_css

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
        .main-app-title.gradient-title-obsidian {
            background: linear-gradient(135deg, #f1f5f9 0%, #c084fc 50%, #38bdf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }
        .main-app-title.gradient-title-corporate {
            background: linear-gradient(135deg, #ffffff 0%, #60a5fa 50%, #818cf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }
        .main-app-subtitle {
            font-size: 1.1rem !important;
            margin-bottom: 1.25rem !important;
            line-height: 1.5 !important;
            text-align: center !important;
        }

        /* Theme Segmented Button Common Styling */
        div.st-key-theme_btn_obsidian button,
        div.st-key-theme_btn_corporate button {
            border-radius: 9999px !important;
            min-height: 44px !important;
            font-size: 0.92rem !important;
            font-weight: 700 !important;
            padding: 10px 20px !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        div.st-key-theme_btn_obsidian button:hover,
        div.st-key-theme_btn_corporate button:hover {
            transform: translateY(-2px) !important;
            filter: brightness(1.1) !important;
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
            border: 3px solid rgba(56, 189, 248, 0.2);
            border-radius: 50%;
            border-top: 3px solid #38bdf8;
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
            div.st-key-theme_btn_obsidian button,
            div.st-key-theme_btn_corporate button {
                font-size: 0.84rem !important;
                padding: 8px 12px !important;
                min-height: 40px !important;
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


def inject_header_element(theme_mode="corporate"):
    if theme_mode == "obsidian":
        gradient_class = "gradient-title-obsidian"
        sub_color = "#a5b4fc"
    else:
        gradient_class = "gradient-title-corporate"
        sub_color = "#94a3b8"

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


def inject_footer_element(theme_mode="corporate"):
    if theme_mode == "obsidian":
        border_color = "rgba(139, 92, 246, 0.2)"
        text_color = "#a5b4fc"
    else:
        border_color = "rgba(59, 130, 246, 0.2)"
        text_color = "#94a3b8"

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
