import streamlit as st
from ai.seo import generate_seo_blog
from database.database import get_setting
from ui.style import page_header
from ai.ollama import OllamaError


def render():
    page_header('SEO Blog Writer', 'Generate SEO-ready blog drafts with title, meta, outline, FAQs, and image prompts.')
    c1, c2 = st.columns(2)
    with c1:
        keyword = st.text_input('Main SEO keyword')
    with c2:
        destination = st.text_input('Destination or region')
    model = get_setting('seo_blog_model', 'llama3.1:latest')
    st.caption(f'Model: {model}')
    if st.button('Generate SEO Blog') and keyword.strip():
        with st.spinner('Writing blog...'):
            output = generate_seo_blog(keyword, destination, model=model)
        st.markdown('<div class="section-title">Generated Blog</div>', unsafe_allow_html=True)
        st.markdown(output)
        st.download_button('Download Blog TXT', output, file_name=f'{keyword.replace(" ", "_")}_blog.txt')
