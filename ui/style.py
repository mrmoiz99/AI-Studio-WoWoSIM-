import streamlit as st


def apply_style():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    :root{
        --bg:#070B14;
        --panel:#0B1220;
        --panel-2:#111827;
        --card:#121A2B;
        --card-2:#162033;
        --border:#253044;
        --border-soft:rgba(255,255,255,.08);
        --text:#F8FAFC;
        --muted:#A7B0C2;
        --orange:#FF5F00;
        --orange-2:#FF8A3D;
        --green:#22C55E;
        --red:#EF4444;
        --blue:#60A5FA;
    }

    html, body, [class*="css"]{font-family:'Inter',sans-serif;}

    .stApp{
        background:
            radial-gradient(circle at 18% -8%, rgba(255,95,0,.18), transparent 26%),
            radial-gradient(circle at 88% 2%, rgba(96,165,250,.10), transparent 25%),
            linear-gradient(180deg,#070B14 0%,#0B1220 45%,#070B14 100%);
        color:var(--text);
    }

    .block-container{padding-top:1.2rem;padding-bottom:3rem;max-width:1440px;}

    [data-testid="stSidebar"]{
        background:linear-gradient(180deg,#0B1220 0%,#090D16 100%);
        border-right:1px solid var(--border-soft);
        box-shadow:12px 0 40px rgba(0,0,0,.22);
    }
    [data-testid="stSidebar"] *{color:var(--text)!important;}
    [data-testid="stSidebar"] .stRadio label{color:var(--muted)!important;}
    [data-testid="stSidebar"] [role="radiogroup"] label{
        padding:9px 12px;border-radius:13px;margin:3px 0;border:1px solid transparent;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover{
        background:rgba(255,95,0,.10);border-color:rgba(255,95,0,.25);
    }

    .app-logo{display:flex;align-items:center;gap:12px;margin:8px 0 18px;}
    .logo-dot{width:42px;height:42px;border-radius:14px;background:linear-gradient(135deg,var(--orange),var(--orange-2));display:flex;align-items:center;justify-content:center;font-weight:900;box-shadow:0 18px 40px rgba(255,95,0,.35);}
    .logo-title{font-size:17px;font-weight:900;letter-spacing:-.03em;}
    .logo-sub{font-size:12px;color:var(--muted)!important;margin-top:2px;}
    .side-box{background:#111827;border:1px solid var(--border);border-radius:18px;padding:14px;margin:16px 0;}
    .side-small{font-size:12px;color:var(--muted)!important;line-height:1.55;}

    .topbar{display:flex;align-items:center;justify-content:space-between;margin:2px 0 18px;}
    .crumb{color:var(--muted);font-size:13px;font-weight:700;}
    .status-pill{display:inline-flex;align-items:center;gap:8px;background:rgba(34,197,94,.10);border:1px solid rgba(34,197,94,.25);color:#86EFAC!important;border-radius:999px;padding:8px 12px;font-size:12px;font-weight:800;}
    .status-dot{width:8px;height:8px;border-radius:999px;background:#22C55E;box-shadow:0 0 14px #22C55E;}

    .hero{
        position:relative;overflow:hidden;
        background:
            radial-gradient(circle at 88% 22%,rgba(255,255,255,.22),transparent 22%),
            linear-gradient(135deg,#FF5F00 0%,#FF7624 55%,#FF9A4D 100%);
        border:1px solid rgba(255,255,255,.16);
        border-radius:30px;
        padding:34px 36px;
        color:white;
        margin-bottom:22px;
        box-shadow:0 25px 80px rgba(255,95,0,.24);
    }
    .hero h1{font-size:42px;line-height:1.04;margin:0 0 10px;color:white;font-weight:900;letter-spacing:-.05em;}
    .hero p{font-size:16px;line-height:1.65;margin:0;max-width:860px;color:rgba(255,255,255,.94)!important;font-weight:600;}
    .kicker{font-size:12px;text-transform:uppercase;letter-spacing:.14em;font-weight:900;color:rgba(255,255,255,.86)!important;margin-bottom:10px;}

    .section-title{font-size:28px;font-weight:900;color:var(--text)!important;letter-spacing:-.04em;margin:6px 0 8px;}
    .section-subtitle{color:var(--muted)!important;font-size:14px;margin-bottom:18px;line-height:1.6;}

    .metric-card,.glass-card,.content-card{
        background:linear-gradient(180deg,rgba(18,26,43,.98),rgba(15,23,38,.98));
        border:1px solid var(--border);
        border-radius:22px;
        padding:20px;
        box-shadow:0 18px 45px rgba(0,0,0,.22);
        margin-bottom:16px;
    }
    .metric-label{color:var(--muted)!important;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;}
    .metric-value{font-size:38px;font-weight:900;color:var(--text)!important;line-height:1;margin-top:10px;}
    .metric-note{color:var(--muted)!important;font-size:13px;margin-top:8px;}

    .workflow-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin:18px 0;}
    .workflow-step{background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:18px;padding:16px;min-height:104px;}
    .workflow-num{width:30px;height:30px;border-radius:10px;background:rgba(255,95,0,.15);color:var(--orange)!important;display:flex;align-items:center;justify-content:center;font-weight:900;margin-bottom:12px;}
    .workflow-step b{color:var(--text)!important;font-size:14px;}
    .workflow-step p{color:var(--muted)!important;font-size:12px;line-height:1.5;margin:6px 0 0;}

    .trend-card{background:linear-gradient(180deg,#121A2B,#101827);border:1px solid var(--border);border-radius:20px;padding:16px;margin-bottom:12px;}
    .trend-title{font-size:17px;font-weight:900;color:var(--text)!important;}
    .trend-meta{font-size:12px;color:var(--muted)!important;margin-top:6px;}
    .score-pill{display:inline-flex;background:rgba(255,95,0,.12);border:1px solid rgba(255,95,0,.28);color:#FFB083!important;border-radius:999px;padding:5px 10px;font-size:12px;font-weight:900;margin-top:10px;}
    .post-caption{background:#0B1220;border:1px solid var(--border);border-radius:16px;padding:14px;color:var(--text)!important;line-height:1.7;}

    h1,h2,h3,h4,h5,h6,p,span,li,label,div{color:var(--text);}
    .stMarkdown, .stMarkdown p, .stMarkdown li{color:var(--text)!important;}
    .stCaption, caption, [data-testid="stCaptionContainer"]{color:var(--muted)!important;}
    hr{border-color:var(--border-soft)!important;}

    div[data-testid="stMetric"]{
        background:linear-gradient(180deg,#121A2B,#101827);
        border:1px solid var(--border);
        border-radius:20px;
        padding:18px;
        box-shadow:0 14px 38px rgba(0,0,0,.20);
    }
    div[data-testid="stMetricLabel"] p{color:var(--muted)!important;font-weight:800;}
    div[data-testid="stMetricValue"]{color:var(--text)!important;font-weight:900;}

    .stButton button, .stDownloadButton button{
        background:linear-gradient(135deg,var(--orange),var(--orange-2));
        color:white!important;border:0;border-radius:14px;font-weight:900;padding:.72rem 1.1rem;
        box-shadow:0 14px 28px rgba(255,95,0,.24);
    }
    .stButton button:hover, .stDownloadButton button:hover{filter:brightness(1.08);color:white!important;border:0;}

    input, textarea, [data-baseweb="select"]>div{
        background:#111A2E!important;color:var(--text)!important;border:1px solid var(--border)!important;border-radius:14px!important;
    }
    [data-baseweb="select"] span{color:var(--text)!important;}
    textarea::placeholder, input::placeholder{color:#667085!important;}

    [data-testid="stExpander"]{background:#121A2B!important;border:1px solid var(--border)!important;border-radius:18px!important;overflow:hidden;}
    [data-testid="stExpander"] *{color:var(--text)!important;}
    [data-testid="stDataFrame"]{border:1px solid var(--border);border-radius:16px;overflow:hidden;}
    .stAlert{border-radius:16px;}
    div[data-testid="stCodeBlock"]{border-radius:16px!important;border:1px solid var(--border)!important;}

    @media (max-width:1100px){.workflow-grid{grid-template-columns:repeat(2,1fr);} .hero h1{font-size:34px;}}
    </style>
    ''', unsafe_allow_html=True)


def page_header(title, subtitle=None, kicker='WoWoSIM Automation'):
    st.markdown(f'''<div class="topbar"><div class="crumb">{kicker}</div><div class="status-pill"><span class="status-dot"></span> Local Mode</div></div>''', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)
