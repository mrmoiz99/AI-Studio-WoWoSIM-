import streamlit as st
from ai.campaign import build_campaign
from database.database import insert_campaign, list_campaigns, get_setting
from ui.style import page_header
from ai.ollama import OllamaError


def render():
    page_header('AI Campaign Builder', 'Create a complete WoWoSIM campaign from one brief and save it for reuse.')
    brief = st.text_area('Campaign brief', placeholder='Example: FIFA 2026 travel campaign for USA, Canada and Mexico visitors', height=140)
    model = get_setting('campaign_builder_model', 'llama3.1:latest')
    st.caption(f'Model: {model}')
    if st.button('Generate Campaign') and brief.strip():
        with st.spinner('Building campaign...'):
            output = build_campaign(brief, model=model)
            insert_campaign(brief[:60], brief, output)
        st.success('Campaign saved.')
        st.markdown(f'<div class="content-card">{output}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Saved Campaigns</div>', unsafe_allow_html=True)
    campaigns = list_campaigns()
    if not campaigns:
        st.info('No campaigns saved yet.')
    for c in campaigns:
        with st.expander(c['name']):
            st.caption(c['created_at'])
            st.write(c['output'])
