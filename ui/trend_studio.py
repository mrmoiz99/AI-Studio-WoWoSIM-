import streamlit as st
from trends.collector import collect_trends
from database.database import list_trends
from ui.style import page_header


def render():
    page_header('Trend Collector', 'Collect fresh topics from free sources and rank them by travel and WoWoSIM relevance.')
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="glass-card"><h3>Collect Free Trends</h3><p class="section-subtitle">Uses free RSS/web sources. No paid API key required.</p></div>', unsafe_allow_html=True)
        if st.button('Collect Free Trends Now'):
            with st.spinner('Collecting trends...'):
                items = collect_trends()
            st.success(f'Collected {len(items)} trends.')
    with col2:
        st.markdown('<div class="glass-card"><h3>Scoring Logic</h3><p class="section-subtitle">Higher scores mean better fit for travel, eSIM, events, airports, and international connectivity.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Saved Trends</div>', unsafe_allow_html=True)
    trends = list_trends(100)
    if not trends:
        st.info('No trends saved yet. Click Collect Free Trends Now.')
    for t in trends:
        st.markdown(f'<div class="trend-card"><div class="trend-title">#{t["id"]} {t["title"]}</div><div class="trend-meta">Source: {t["source"]} • Created: {t["created_at"]}</div><span class="score-pill">Score {t["score"]}</span></div>', unsafe_allow_html=True)
