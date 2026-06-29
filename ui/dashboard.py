import streamlit as st
from database.database import list_trends, list_posts, list_images


def render():
    trends = list_trends(1000)
    posts = list_posts(1000)
    images = list_images(1000)
    approved = [p for p in posts if p['status'] == 'approved']

    st.markdown('''
    <div class="hero">
        <div class="kicker">Version 1 • Local PC • No API Keys</div>
        <h1>WoWoSIM AI Marketing Automation</h1>
        <p>Collect free trends, score them, generate WoWoSIM captions, create image prompts, generate visuals, approve content, and manually publish to social media.</p>
    </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Trends Saved</div><div class="metric-value">{len(trends)}</div><div class="metric-note">Free RSS sources</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Posts Created</div><div class="metric-value">{len(posts)}</div><div class="metric-note">Drafts and approvals</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Approved</div><div class="metric-value">{len(approved)}</div><div class="metric-note">Ready to publish</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Images</div><div class="metric-value">{len(images)}</div><div class="metric-note">Saved locally</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Automation Workflow</div><div class="section-subtitle">This version stays 100% local and avoids paid APIs.</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="workflow-grid">
        <div class="workflow-step"><div class="workflow-num">1</div><b>Collect</b><p>Pull trending topics from free sources.</p></div>
        <div class="workflow-step"><div class="workflow-num">2</div><b>Score</b><p>Rank trends by WoWoSIM fit.</p></div>
        <div class="workflow-step"><div class="workflow-num">3</div><b>Generate</b><p>Create captions, hashtags, and prompts.</p></div>
        <div class="workflow-step"><div class="workflow-num">4</div><b>Visualize</b><p>Generate or export image prompts.</p></div>
        <div class="workflow-step"><div class="workflow-num">5</div><b>Approve</b><p>Review each post before publishing.</p></div>
        <div class="workflow-step"><div class="workflow-num">6</div><b>Publish</b><p>Download assets and post manually.</p></div>
    </div>
    ''', unsafe_allow_html=True)

    if trends:
        st.markdown('<div class="section-title">Latest Trends</div>', unsafe_allow_html=True)
        for t in trends[:5]:
            st.markdown(f'<div class="trend-card"><div class="trend-title">{t["title"]}</div><div class="trend-meta">Source: {t["source"]} • Saved: {t["created_at"]}</div><span class="score-pill">Score {t["score"]}</span></div>', unsafe_allow_html=True)
