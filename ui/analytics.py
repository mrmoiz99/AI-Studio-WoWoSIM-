import streamlit as st
import pandas as pd
from database.database import list_trends, list_posts, list_images
from ui.style import page_header


def render():
    page_header('Analytics', 'Track generated assets, approval status, and local content performance indicators.')
    trends = list_trends(1000)
    posts = list_posts(1000)
    images = list_images(1000)
    approved = [p for p in posts if p['status'] == 'approved']
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Trends', len(trends))
    c2.metric('Posts', len(posts))
    c3.metric('Approved', len(approved))
    c4.metric('Images', len(images))

    if posts:
        df = pd.DataFrame([dict(p) for p in posts])
        st.markdown('<div class="section-title">Posts by Status</div>', unsafe_allow_html=True)
        st.bar_chart(df['status'].value_counts())
        st.markdown('<div class="section-title">Recent Posts</div>', unsafe_allow_html=True)
        st.dataframe(df[['id', 'platform', 'title', 'status', 'created_at']], use_container_width=True)
    else:
        st.info('No posts yet.')
