import streamlit as st
from ai.image_engine import generate_creative_set
from ai.design_templates import TEMPLATES
from database.database import list_posts, list_images, get_setting
from ui.style import page_header


def render():
    page_header(
        'AI Creative Director',
        'Phase 3: Research Agent, Campaign Planner, Scene Planner, prompt variations, image scoring, and WoWoSIM brand composition.'
    )
    posts = list_posts(100)
    labels = {f"#{p['id']} {p['title'] or p['trend_title']}": p for p in posts if p['image_prompt']}

    left, right = st.columns([1, 1])
    with left:
        st.markdown('''
        <div class="glass-card">
            <h3>Marketing Brain Pipeline</h3>
            <p class="section-subtitle">
            Phase 3 no longer sends a single vague prompt to the image model. It researches the trend, plans the campaign, creates a scene brief, generates prompt variations, scores the results, then applies WoWoSIM branding.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        provider = st.selectbox(
            'Image Provider',
            ['Use Settings Default', 'pollinations', 'gemini'],
            help='Gemini needs image quota/billing. Pollinations is free but less predictable.'
        )
        selected_provider = None if provider == 'Use Settings Default' else provider
        active_provider = selected_provider or get_setting('image_provider', 'pollinations')
        st.caption(f'Active provider: {active_provider}')

        template_name = st.selectbox('Design Template', list(TEMPLATES.keys()))
        variations = st.slider('Background variations', 1, 4, 4)
        compose = st.checkbox('Add WoWoSIM branded design layer', value=True)
        cta = st.text_input('CTA text', value=TEMPLATES[template_name]['cta'])

        if labels:
            selected = st.selectbox('Generate from post image prompt', list(labels.keys()))
            size = st.selectbox('Size', ['1080x1350', '1024x1024', '1024x768'])
            if st.button('Generate Creative Set'):
                p = labels[selected]
                w, h = map(int, size.split('x'))
                with st.spinner(f'Marketing Brain is researching, planning, generating {variations} option(s), scoring, and composing final designs...'):
                    try:
                        result = generate_creative_set(
                            p['image_prompt'],
                            post_id=p['id'],
                            width=w,
                            height=h,
                            provider=selected_provider,
                            title=p['title'] or p['trend_title'],
                            caption=p['caption'],
                            cta=cta,
                            compose=compose,
                            template_name=template_name,
                            variations=variations,
                        )
                        st.success(f'Creative set generated. Best option: #{result["best"]["index"]} with score {result["best"]["score"]}.')
                        st.session_state['last_creative_set'] = result
                    except Exception as e:
                        st.error('Image generation failed.')
                        st.code(str(e))
                        if active_provider == 'gemini':
                            st.info('Gemini image generation may require paid quota. Switch to Pollinations or enable fallback in Settings.')
        else:
            st.info('Generate a post with an image prompt first.')

    with right:
        if labels:
            p = labels[selected]
            with st.expander('Selected Image Prompt', expanded=True):
                st.write(p['image_prompt'])
            with st.expander('What Phase 3 adds', expanded=False):
                st.markdown('''
1. **Research Agent** finds the travel/eSIM angle.
2. **Campaign Planner** chooses campaign type, template, tone, and CTA.
3. **Scene Planner** builds a structured photography brief.
4. **Prompt Engine** creates provider-safe prompt variations.
5. **Quality Scorer** ranks results using sharpness, brightness, text-space, and composition signals.
6. **Brand Composer** adds consistent WoWoSIM design on top of the best background.
''')

    if 'last_creative_set' in st.session_state:
        result = st.session_state['last_creative_set']
        st.markdown('<div class="section-title">Best Creative</div>', unsafe_allow_html=True)
        st.image(result['best']['final_path'], caption=f"Best Option #{result['best']['index']} • Score {result['best']['score']} • {result['best']['provider']}", use_container_width=True)

        with st.expander('Marketing Brain Details', expanded=False):
            tabs = st.tabs(['Research', 'Campaign Plan', 'Scene Plan'])
            with tabs[0]:
                st.json(result.get('research', {}))
            with tabs[1]:
                st.json(result.get('campaign', {}))
            with tabs[2]:
                st.json(result.get('scene', {}))

        st.markdown('<div class="section-title">All Creative Options</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        for i, item in enumerate(result['outputs']):
            with cols[i % 4]:
                st.image(item['final_path'], caption=f"Option #{item['index']} • Score {item['score']}", use_container_width=True)
                with st.expander('Score details'):
                    st.json(item.get('score_details', {}))
                with st.expander('Background versions'):
                    st.caption('Raw AI background')
                    st.image(item.get('raw_path'), use_container_width=True)
                    st.caption('Processed background used by composer')
                    st.image(item.get('processed_path'), use_container_width=True)
                with open(item['final_path'], 'rb') as f:
                    st.download_button(
                        'Download',
                        data=f.read(),
                        file_name=f"wowosim_creative_option_{item['index']}.png",
                        mime='image/png',
                        key=f"download_creative_{item['index']}_{item['score']}"
                    )
                with st.expander('Prompt'):
                    st.write(item['prompt'])

    st.markdown('<div class="section-title">Image Library</div>', unsafe_allow_html=True)
    images = list_images(50)
    if not images:
        st.info('No images generated yet.')
    else:
        cols = st.columns(4)
        for i, img in enumerate(images):
            with cols[i % 4]:
                st.image(img['path'], caption=img['created_at'], use_container_width=True)
