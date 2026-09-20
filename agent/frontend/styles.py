import streamlit as st

def inject_premium_styles(theme_mode="corporate"):
    active_mode = "light" if theme_mode == "light" else "corporate"

    # ================= 1. CORPORATE TRUST (Deep Blues & Slate) — UNCHANGED =================
    theme_corporate_css = """
        /* Corporate Trust - Deep Slate to Navy Blue */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
            color: #f8fafc !important;
            min-height: 100vh;
            transition: background 0.35s ease, color 0.25s ease;
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

        /* Navigation Segmented Control (Corporate) */
        div[data-testid="stSegmentedControl"] {
            margin: 1.5rem 0 1.75rem 0 !important;
        }
        div[data-testid="stSegmentedControl"] button {
            background: rgba(30, 41, 59, 0.55) !important;
            border: 1px solid rgba(59, 130, 246, 0.25) !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
            color: #cbd5e1 !important;
            font-size: 0.95rem !important;
        }
        div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
            border-color: #60a5fa !important;
            color: #ffffff !important;
            box-shadow: 0 4px 18px rgba(37, 99, 235, 0.45) !important;
            font-weight: 700 !important;
        }

        /* Inputs, Textareas & Selects (Corporate Dark Mode) */
        .stApp .stTextArea,
        .stApp .stTextInput,
        .stApp .stSelectbox,
        .stApp div[data-testid="stTextArea"],
        .stApp div[data-testid="stTextInput"],
        .stApp div[data-testid="stSelectbox"],
        .stApp div[data-testid="stTextArea"] > div,
        .stApp div[data-testid="stTextInput"] > div,
        .stApp div[data-testid="stSelectbox"] > div,
        .stApp div[data-testid="stTextArea"] div[data-baseweb="textarea"],
        .stApp div[data-testid="stTextArea"] div[data-baseweb="base-input"],
        .stApp div[data-testid="stTextInput"] div[data-baseweb="input"],
        .stApp div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"],
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"] div[role="combobox"],
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"] div[role="combobox"] > div,
        .stApp div[data-baseweb="textarea"],
        .stApp div[data-baseweb="textarea"] > div,
        .stApp div[data-baseweb="input"],
        .stApp div[data-baseweb="input"] > div,
        .stApp div[data-baseweb="base-input"],
        .stApp div[data-baseweb="base-input"] > div,
        .stApp div[data-baseweb="select"],
        .stApp div[data-baseweb="select"] > div,
        .stApp div[data-baseweb="select"] div {
            background-color: #0f172a !important;
            background: #0f172a !important;
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
        }

        .stApp div[data-testid="stTextArea"] div[data-baseweb="textarea"],
        .stApp div[data-testid="stTextInput"] div[data-baseweb="input"],
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            border: 1.5px solid rgba(59, 130, 246, 0.35) !important;
            border-radius: 12px !important;
            transition: all 0.25s ease !important;
        }

        .stApp textarea,
        .stApp input {
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
            background-color: #0f172a !important;
            background: #0f172a !important;
            font-size: 0.95rem !important;
        }

        .stApp textarea::placeholder,
        .stApp input::placeholder {
            color: #64748b !important;
            -webkit-text-fill-color: #64748b !important;
        }

        .stApp div[data-testid="stSelectbox"] span,
        .stApp div[data-testid="stSelectbox"] div,
        .stApp div[data-baseweb="select"] span,
        .stApp div[data-baseweb="select"] div,
        .stApp div[data-baseweb="select"] [role="combobox"] {
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
        }

        .stApp div[data-testid="stSelectbox"] svg {
            fill: #94a3b8 !important;
        }

        .stApp div[data-baseweb="textarea"]:focus-within,
        .stApp div[data-baseweb="input"]:focus-within,
        .stApp div[data-baseweb="select"] > div:focus-within,
        .stApp div[data-testid="stTextArea"] textarea:focus,
        .stApp div[data-testid="stTextInput"] input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
        }

        /* Primary Action Buttons */
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

        /* Floating Theme Toggle (Corporate) */
        div.st-key-theme_toggle_btn button {
            background: rgba(30, 41, 59, 0.85) !important;
            border: 1px solid rgba(96, 165, 250, 0.5) !important;
            color: #93c5fd !important;
            border-radius: 9999px !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            padding: 6px 16px !important;
            min-height: 36px !important;
            width: auto !important;
            letter-spacing: 0.3px !important;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
            backdrop-filter: blur(8px) !important;
        }
        div.st-key-theme_toggle_btn button p,
        div.st-key-theme_toggle_btn button span {
            color: #93c5fd !important;
            -webkit-text-fill-color: #93c5fd !important;
            font-weight: 600 !important;
        }
        div.st-key-theme_toggle_btn button:hover {
            background: rgba(37, 99, 235, 0.85) !important;
            border-color: #60a5fa !important;
            transform: none !important;
            filter: brightness(1.12) !important;
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
            border-color: #38bdf8 !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3) !important;
        }

        /* Clickable Metric Card Buttons (Corporate) */
        .stApp div[class*="st-key-btn_metric_"] .stButton > button,
        .stApp div[class*="st-key-btn_metric_"] button,
        div.st-key-btn_metric_domains button,
        div.st-key-btn_metric_seo_issues button,
        div.st-key-btn_metric_critical_issues button {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
            border: 1px solid rgba(59, 130, 246, 0.35) !important;
            border-radius: 18px !important;
            padding: 1.5rem 1rem !important;
            min-height: 120px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            width: 100% !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button:hover,
        .stApp div[class*="st-key-btn_metric_"] button:hover {
            transform: translateY(-4px) !important;
            border-color: #38bdf8 !important;
            box-shadow: 0 12px 35px rgba(56, 189, 248, 0.25) !important;
            filter: brightness(1.08) !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button > div,
        .stApp div[class*="st-key-btn_metric_"] .stButton > button div[data-testid="stMarkdownContainer"] {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            gap: 4px !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button div[data-testid="stMarkdownContainer"] p {
            display: block !important;
            text-align: center !important;
            width: 100% !important;
            margin: 0 !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button div[data-testid="stMarkdownContainer"] p:first-of-type {
            font-size: 0.85rem !important;
            color: #94a3b8 !important;
            -webkit-text-fill-color: #94a3b8 !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin: 0 0 0.4rem 0 !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button div[data-testid="stMarkdownContainer"] p:last-of-type {
            font-size: 2.35rem !important;
            font-weight: 800 !important;
            line-height: 1.1 !important;
            margin: 0 !important;
        }
        .stApp div[class*="st-key-btn_metric_domains"] .stButton > button div[data-testid="stMarkdownContainer"] p:last-of-type {
            color: #38bdf8 !important;
            -webkit-text-fill-color: #38bdf8 !important;
        }
        .stApp div[class*="st-key-btn_metric_seo_issues"] .stButton > button div[data-testid="stMarkdownContainer"] p:last-of-type {
            color: #818cf8 !important;
            -webkit-text-fill-color: #818cf8 !important;
        }
        .stApp div[class*="st-key-btn_metric_critical_issues"] .stButton > button div[data-testid="stMarkdownContainer"] p:last-of-type {
            color: #f87171 !important;
            -webkit-text-fill-color: #f87171 !important;
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

    # ================= 2. ENTERPRISE SaaS LIGHT MODE (Semrush / Linear / Notion Aesthetic) =================
    theme_light_css = """
        /* Import Inter font for premium SaaS typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Enterprise Light Mode — Slate-100 page, white cards */
        .stApp {
            background: #F1F5F9 !important;
            color: #0F172A !important;
            min-height: 100vh;
            transition: background 0.35s ease, color 0.25s ease;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }

        /* Typography — dark charcoal, no harsh pure black */
        h1 {
            background: linear-gradient(135deg, #4F46E5 0%, #0EA5E9 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }
        h2 { color: #0F172A !important; font-weight: 700 !important; }
        h3, h4 { color: #1E293B !important; font-weight: 700 !important; }
        h5, h6 { color: #334155 !important; }
        label { color: #374151 !important; font-weight: 500 !important; }
        p, li { color: #475569 !important; line-height: 1.7 !important; }

        /* White card with elegant shadow — no glassmorphism */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 16px !important;
            padding: 1.8rem !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04) !important;
            margin-bottom: 1.5rem !important;
        }

        /* Recommendation cards — clean left-border style (Linear App) */
        .recommendation-item {
            background: #F8FAFC !important;
            border-left: 4px solid #4F46E5 !important;
            border-top: 1px solid #E2E8F0 !important;
            border-right: 1px solid #E2E8F0 !important;
            border-bottom: 1px solid #E2E8F0 !important;
            border-radius: 0 10px 10px 0 !important;
            padding: 1rem 1.25rem !important;
            margin: 0.75rem 0 !important;
            color: #334155 !important;
            font-size: 0.95rem !important;
        }

        /* Static metric cards */
        .metric-card {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 16px !important;
            padding: 1.6rem !important;
            text-align: center !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04) !important;
            transition: transform 0.25s ease, box-shadow 0.25s ease !important;
        }
        .metric-card:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.12) !important;
        }
        .metric-label {
            font-size: 0.78rem !important;
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            margin-bottom: 0.6rem !important;
        }
        .metric-value {
            font-size: 2.35rem !important;
            font-weight: 800 !important;
            color: #4F46E5 !important;
            -webkit-text-fill-color: #4F46E5 !important;
        }

        /* Navigation Segmented Control (Light) — white pill bar */
        div[data-testid="stSegmentedControl"] {
            margin: 1.5rem 0 1.75rem 0 !important;
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            padding: 4px !important;
        }
        div[data-testid="stSegmentedControl"] button {
            background: transparent !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 9px 18px !important;
            font-weight: 500 !important;
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-size: 0.9rem !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
            background: #4F46E5 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            box-shadow: 0 2px 8px rgba(79, 70, 229, 0.35) !important;
            font-weight: 700 !important;
        }
        div[data-testid="stSegmentedControl"] button:hover:not([aria-checked="true"]) {
            background: #F1F5F9 !important;
            color: #1E293B !important;
            -webkit-text-fill-color: #1E293B !important;
        }

        /* Inputs, Textareas & Selects (Light Mode) */
        .stApp .stTextArea,
        .stApp .stTextInput,
        .stApp .stSelectbox,
        .stApp div[data-testid="stTextArea"],
        .stApp div[data-testid="stTextInput"],
        .stApp div[data-testid="stSelectbox"],
        .stApp div[data-testid="stTextArea"] > div,
        .stApp div[data-testid="stTextInput"] > div,
        .stApp div[data-testid="stSelectbox"] > div,
        .stApp div[data-testid="stTextArea"] div[data-baseweb="textarea"],
        .stApp div[data-testid="stTextArea"] div[data-baseweb="base-input"],
        .stApp div[data-testid="stTextInput"] div[data-baseweb="input"],
        .stApp div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"],
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"] div[role="combobox"],
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"] div[role="combobox"] > div,
        .stApp div[data-baseweb="textarea"],
        .stApp div[data-baseweb="textarea"] > div,
        .stApp div[data-baseweb="input"],
        .stApp div[data-baseweb="input"] > div,
        .stApp div[data-baseweb="base-input"],
        .stApp div[data-baseweb="base-input"] > div,
        .stApp div[data-baseweb="select"],
        .stApp div[data-baseweb="select"] > div,
        .stApp div[data-baseweb="select"] div {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: #0F172A !important;
            -webkit-text-fill-color: #0F172A !important;
        }

        .stApp div[data-testid="stTextArea"] div[data-baseweb="textarea"],
        .stApp div[data-testid="stTextInput"] div[data-baseweb="input"],
        .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            border: 1.5px solid #CBD5E1 !important;
            border-radius: 10px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
            transition: all 0.2s ease !important;
        }

        .stApp textarea,
        .stApp input {
            color: #0F172A !important;
            -webkit-text-fill-color: #0F172A !important;
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            font-size: 0.95rem !important;
        }

        .stApp textarea::placeholder,
        .stApp input::placeholder {
            color: #94A3B8 !important;
            -webkit-text-fill-color: #94A3B8 !important;
        }

        .stApp div[data-testid="stSelectbox"] span,
        .stApp div[data-testid="stSelectbox"] div,
        .stApp div[data-baseweb="select"] span,
        .stApp div[data-baseweb="select"] div,
        .stApp div[data-baseweb="select"] [role="combobox"] {
            color: #0F172A !important;
            -webkit-text-fill-color: #0F172A !important;
        }

        .stApp div[data-testid="stSelectbox"] svg {
            fill: #64748B !important;
        }

        .stApp div[data-baseweb="textarea"]:focus-within,
        .stApp div[data-baseweb="input"]:focus-within,
        .stApp div[data-baseweb="select"] > div:focus-within,
        .stApp div[data-testid="stTextArea"] textarea:focus,
        .stApp div[data-testid="stTextInput"] input:focus {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
        }

        /* Primary buttons — solid indigo */
        div.stButton > button {
            background: #4F46E5 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 13px 28px !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            letter-spacing: 0.3px !important;
        }
        div.stButton > button p,
        div.stButton > button span,
        div.stButton > button div {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 600 !important;
        }
        div.stButton > button:hover {
            background: #4338CA !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
            filter: none !important;
        }

        /* Floating Theme Toggle (Light Mode) */
        div.st-key-theme_toggle_btn button {
            background: #FFFFFF !important;
            border: 1.5px solid #CBD5E1 !important;
            color: #475569 !important;
            border-radius: 9999px !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            padding: 6px 16px !important;
            min-height: 36px !important;
            width: auto !important;
            letter-spacing: 0.3px !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
            backdrop-filter: none !important;
        }
        div.st-key-theme_toggle_btn button p,
        div.st-key-theme_toggle_btn button span {
            color: #475569 !important;
            -webkit-text-fill-color: #475569 !important;
            font-weight: 600 !important;
        }
        div.st-key-theme_toggle_btn button:hover {
            background: #F1F5F9 !important;
            border-color: #94A3B8 !important;
            color: #1E293B !important;
            transform: none !important;
            filter: none !important;
        }

        /* Clear Scan Button (light mode) */
        div.st-key-clear_scan_btn button,
        div[class*="st-key-clear_scan_btn"] button {
            background: #FFF5F5 !important;
            border: 1px solid #FCA5A5 !important;
            color: #DC2626 !important;
            border-radius: 10px !important;
            padding: 10px 18px !important;
        }
        div.st-key-clear_scan_btn button p,
        div.st-key-clear_scan_btn button span {
            color: #DC2626 !important;
            -webkit-text-fill-color: #DC2626 !important;
        }

        /* Download button (light) */
        div.stDownloadButton > button {
            background: #FFFFFF !important;
            color: #4F46E5 !important;
            border: 1.5px solid #4F46E5 !important;
            border-radius: 10px !important;
            padding: 11px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
        }
        div.stDownloadButton > button:hover {
            background: #EEF2FF !important;
            border-color: #4338CA !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.18) !important;
        }

        /* Clickable Metric Card Buttons (Light Mode) */
        .stApp div[class*="st-key-btn_metric_"] .stButton > button,
        .stApp div[class*="st-key-btn_metric_"] button,
        div.st-key-btn_metric_domains button,
        div.st-key-btn_metric_seo_issues button,
        div.st-key-btn_metric_critical_issues button {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 16px !important;
            padding: 1.5rem 1rem !important;
            min-height: 120px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            width: 100% !important;
        }
        .stApp div[class*="st-key-btn_metric_domains"] .stButton > button {
            border-bottom: 3px solid #0EA5E9 !important;
        }
        .stApp div[class*="st-key-btn_metric_seo_issues"] .stButton > button {
            border-bottom: 3px solid #6366F1 !important;
        }
        .stApp div[class*="st-key-btn_metric_critical_issues"] .stButton > button {
            border-bottom: 3px solid #EF4444 !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button:hover,
        .stApp div[class*="st-key-btn_metric_"] button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15) !important;
            filter: none !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button > div,
        .stApp div[class*="st-key-btn_metric_"] .stButton > button div[data-testid="stMarkdownContainer"] {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            gap: 4px !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button div[data-testid="stMarkdownContainer"] p {
            display: block !important;
            text-align: center !important;
            width: 100% !important;
            margin: 0 !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button div[data-testid="stMarkdownContainer"] p:first-of-type {
            font-size: 0.75rem !important;
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            margin: 0 0 0.5rem 0 !important;
        }
        .stApp div[class*="st-key-btn_metric_"] .stButton > button div[data-testid="stMarkdownContainer"] p:last-of-type {
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            line-height: 1.1 !important;
            margin: 0 !important;
        }
        .stApp div[class*="st-key-btn_metric_domains"] .stButton > button div[data-testid="stMarkdownContainer"] p:last-of-type {
            color: #0EA5E9 !important;
            -webkit-text-fill-color: #0EA5E9 !important;
        }
        .stApp div[class*="st-key-btn_metric_seo_issues"] .stButton > button div[data-testid="stMarkdownContainer"] p:last-of-type {
            color: #6366F1 !important;
            -webkit-text-fill-color: #6366F1 !important;
        }
        .stApp div[class*="st-key-btn_metric_critical_issues"] .stButton > button div[data-testid="stMarkdownContainer"] p:last-of-type {
            color: #EF4444 !important;
            -webkit-text-fill-color: #EF4444 !important;
        }

        /* Browser Mockup Frame (Light — Figma style chrome) */
        .browser-frame {
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            background: #FFFFFF !important;
            overflow: hidden !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
        }
        .browser-header {
            background: #F8FAFC !important;
            padding: 8px 14px !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
            border-bottom: 1px solid #E2E8F0 !important;
        }
        .browser-address {
            background: #FFFFFF !important;
            color: #64748B !important;
            border: 1px solid #E2E8F0 !important;
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

        /* Popovers & dropdowns (light) */
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
        }
        div[data-baseweb="menu"] li:hover, div[role="option"]:hover, div[role="option"][aria-selected="true"] {
            background-color: #EEF2FF !important;
            color: #4F46E5 !important;
        }

        /* DataFrames (light) */
        div[data-testid="stDataFrame"] {
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            background: #FFFFFF !important;
        }
        div[data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
        }

        /* Info & success boxes in light mode */
        div[data-testid="stAlert"] {
            border-radius: 10px !important;
        }

        /* Slider track (light) */
        div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
            background: #4F46E5 !important;
        }
    """

    theme_css = theme_light_css if active_mode == "light" else theme_corporate_css

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
        .main-app-title.gradient-title-light {
            background: linear-gradient(135deg, #4F46E5 0%, #0EA5E9 100%) !important;
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

        /* Floating Theme Toggle — positioned top-right via parent container */
        .theme-toggle-wrapper {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 0.5rem;
        }

        /* Shared toggle button sizing */
        div.st-key-theme_toggle_btn button {
            min-height: 36px !important;
            width: auto !important;
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
        .circular-spinner-light {
            width: 32px;
            height: 32px;
            border: 3px solid rgba(79, 70, 229, 0.15);
            border-radius: 50%;
            border-top: 3px solid #4F46E5;
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
    if theme_mode == "light":
        gradient_class = "gradient-title-light"
        sub_color = "#475569"
    else:  # corporate (dark)
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
    if theme_mode == "light":
        border_color = "#E2E8F0"
        text_color = "#64748B"
    else:  # corporate
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
        2026 Chronflow Made By Patel Rudra J. , All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)
