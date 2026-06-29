import re
import streamlit as st
from database.database import list_trends, insert_post, get_setting
from ai.captions import generate_social_post
from ai.ollama import OllamaError
from ui.style import page_header


def _extract(text, label):
    m = re.search(label + r':\s*(.*?)(?=\n[A-Z ]+:|$)', text, re.S | re.I)
    return m.group(1).strip() if m else ''


def render():
    page_header('Post Generator', 'Turn a trend into complete platform-ready WoWoSIM captions, hashtags, and image prompts.')
    trends = list_trends(100)
    if not trends:
        st.info('Collect trends first from Trend Collector.')
        return

    trend_labels = {f"#{t['id']} {t['title']} | score {t['score']}": t for t in trends}
    left, right = st.columns([1, 1])
    with left:
        st.markdown('<div class="glass-card"><h3>Generation Settings</h3></div>', unsafe_allow_html=True)
        selected = st.selectbox('Choose trend', list(trend_labels.keys()))
        platform = st.selectbox('Platform', ['Instagram', 'Facebook', 'LinkedIn'])
        model = get_setting('social_posts_model', 'llama3.1:latest')
        st.caption(f'Model: {model}')
        generate = st.button('Generate Post')
    with right:
        t = trend_labels[selected]
        st.markdown(f'<div class="trend-card"><div class="trend-title">{t["title"]}</div><div class="trend-meta">Source: {t["source"]}</div><span class="score-pill">Score {t["score"]}</span></div>', unsafe_allow_html=True)

    if generate:
        t = trend_labels[selected]
        try:
            with st.spinner('Generating WoWoSIM post...'):
                raw = generate_social_post(t['title'], platform=platform, model=model)
        except OllamaError as e:
            st.error(str(e))
            return
        title = _extract(raw, 'TITLE') or t['title']
        caption = _extract(raw, 'CAPTION') or raw
        hashtags = _extract(raw, 'HASHTAGS')
        image_prompt = _extract(raw, 'IMAGE PROMPT')
        post_id = insert_post(t['id'], platform, title, caption, hashtags, image_prompt)
        st.success(f'Post saved as draft #{post_id}.')
        st.markdown('<div class="section-title">Generated Post</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="content-card"><h3>{title}</h3><div class="post-caption">{caption}</div><br><b>Hashtags</b><p>{hashtags}</p></div>', unsafe_allow_html=True)
        with st.expander('Image Prompt'):
            st.write(image_prompt)
