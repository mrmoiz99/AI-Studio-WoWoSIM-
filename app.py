import streamlit as st
from dotenv import load_dotenv
from database.database import init_db
from ui.style import apply_style

load_dotenv()
from ui import dashboard, trend_studio, post_generator, content_library, image_studio, campaign_builder, seo_blog, analytics, settings

st.set_page_config(page_title='WoWoSIM AI Automation', page_icon='🟠', layout='wide', initial_sidebar_state='expanded')
init_db()
apply_style()

PAGES = {
    'Dashboard': dashboard.render,
    'Trend Collector': trend_studio.render,
    'Post Generator': post_generator.render,
    'Content Library': content_library.render,
    'AI Creative Director': image_studio.render,
    'Campaign Builder': campaign_builder.render,
    'SEO Blog': seo_blog.render,
    'Analytics': analytics.render,
    'Settings': settings.render,
}

with st.sidebar:
    st.markdown('''
    <div class="app-logo">
        <div class="logo-dot">W</div>
        <div>
            <div class="logo-title">WoWoSIM AI</div>
            <div class="logo-sub">Marketing Automation</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="side-small">Marketing Brain v3 • Local PC • Optional Gemini images</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-box"><b>Quick Setup</b><br><br><code>ollama serve</code><br><code>ollama pull llama3.1:latest</code><br><code>ollama pull qwen3:8b</code><br><code>optional: GEMINI_API_KEY</code></div>', unsafe_allow_html=True)
    choice = st.radio('Navigation', list(PAGES.keys()), label_visibility='collapsed')
    st.markdown('<div class="side-box"><b>Manual Publishing</b><div class="side-small">Generate, approve, download image, copy caption, then post manually to Facebook, Instagram, or LinkedIn.</div></div>', unsafe_allow_html=True)

PAGES[choice]()
