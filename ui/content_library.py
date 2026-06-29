import streamlit as st
from database.database import list_posts, update_post_status
from ui.style import page_header


def render():
    page_header('Content Library & Approval Queue', 'Review generated posts, approve the best ones, and prepare content for manual publishing.')
    q = st.text_input('Search content', placeholder='Search by title, trend, caption, hashtags...')
    posts = list_posts(200, q)
    if not posts:
        st.info('No posts found. Generate content first.')
        return

    st.caption(f'Showing {len(posts)} posts')
    for p in posts:
        status = p['status']
        title = p['title'] or p['trend_title']
        st.markdown(f'<div class="content-card"><div class="trend-title">{title}</div><div class="trend-meta">Platform: {p["platform"]} • Status: {status} • Created: {p["created_at"]}</div><br><div class="post-caption">{p["caption"]}</div><br><b>Hashtags</b><p>{p["hashtags"]}</p></div>', unsafe_allow_html=True)
        with st.expander('Image Prompt'):
            st.write(p['image_prompt'])
        c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
        if c1.button('Approve', key=f"approve_{p['id']}"):
            update_post_status(p['id'], 'approved')
            st.rerun()
        if c2.button('Needs Edit', key=f"edit_{p['id']}"):
            update_post_status(p['id'], 'needs_edit')
            st.rerun()
        if c3.button('Reject', key=f"reject_{p['id']}"):
            update_post_status(p['id'], 'rejected')
            st.rerun()
        c4.download_button('Download Caption', f"{p['caption']}\n\n{p['hashtags']}", file_name=f"post_{p['id']}_caption.txt")
        st.divider()
