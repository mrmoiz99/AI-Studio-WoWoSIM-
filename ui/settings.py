import json
import streamlit as st
from config import DEFAULT_MODELS, BRAND_MEMORY_PATH, ENV_GEMINI_API_KEY
from database.database import upsert_setting, get_setting
from ui.style import page_header


def _save_text_setting(label, key, default, help_text=None):
    val = st.text_input(label, value=get_setting(key, default), help=help_text)
    upsert_setting(key, val.strip())
    return val.strip()


def _masked_key(key: str) -> str:
    key = (key or "").strip()
    if not key:
        return "Not saved"
    if len(key) <= 10:
        return "Saved"
    return f"Saved: {key[:6]}...{key[-4:]}"


def render():
    page_header('Settings & Model Manager', 'Control models, image provider, API keys, and brand memory from one place.')

    st.markdown('<div class="section-title">API Keys</div>', unsafe_allow_html=True)
    with st.container(border=True):
        current_key = get_setting('gemini_api_key', '') or ENV_GEMINI_API_KEY
        st.caption(f"Gemini API Key Status: {_masked_key(current_key)}")
        gemini_key_input = st.text_input(
            'Gemini API Key',
            value='',
            type='password',
            placeholder='Paste your Gemini API key here, then click Save API Keys',
            help='Stored locally in your SQLite database. Leave blank if you do not want to change the saved key.'
        )
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button('Save API Keys', use_container_width=True):
                if gemini_key_input.strip():
                    upsert_setting('gemini_api_key', gemini_key_input.strip())
                    st.success('Gemini API key saved locally.')
                else:
                    st.warning('Paste a key first. Blank input does not overwrite your existing key.')
        with col_b:
            if st.button('Remove Gemini Key', use_container_width=True):
                upsert_setting('gemini_api_key', '')
                st.success('Gemini API key removed from local settings.')
        st.info('Your key is saved only on this PC inside the local SQLite database. Do not share your project folder publicly with the database included.')

    st.markdown('<div class="section-title">Ollama Text Models</div>', unsafe_allow_html=True)
    with st.container(border=True):
        for key, default in DEFAULT_MODELS.items():
            _save_text_setting(key.replace('_', ' ').title(), f'{key}_model', default)

    st.markdown('<div class="section-title">Image Provider</div>', unsafe_allow_html=True)
    with st.container(border=True):
        provider = st.selectbox(
            'Default Image Provider',
            ['gemini', 'pollinations'],
            index=0 if get_setting('image_provider', 'pollinations') == 'gemini' else 1,
            help='Gemini usually gives better backgrounds. Pollinations is free but lower quality.'
        )
        upsert_setting('image_provider', provider)

        col1, col2 = st.columns(2)
        with col1:
            _save_text_setting('Gemini Image Model', 'gemini_image_model', get_setting('gemini_image_model', 'gemini-3.1-flash-image'))
        with col2:
            _save_text_setting('Pollinations Model', 'pollinations_image_model', get_setting('pollinations_image_model', 'turbo'))

        fallback = st.checkbox(
            'Use Pollinations fallback if Gemini fails',
            value=get_setting('image_fallback', 'no') == 'yes',
            help='Turn this off when you only want Gemini. Turn it on if you prefer getting any image instead of an error.'
        )
        upsert_setting('image_fallback', 'yes' if fallback else 'no')

        quality_mode = st.selectbox(
            'Background Quality Mode',
            ['high', 'fast'],
            index=0 if get_setting('background_quality_mode', 'high') == 'high' else 1,
            help='High requests a larger background then crops/sharpens locally. Fast uses the final canvas size directly.'
        )
        upsert_setting('background_quality_mode', quality_mode)

    with st.expander('Recommended setup', expanded=False):
        st.markdown('''
Current free setup:

```text
Default Image Provider: pollinations
Pollinations Model: turbo
Background Quality Mode: high
```

If you enable paid Gemini image quota later, switch Default Image Provider to gemini. The app still adds WoWoSIM branding/text separately.
''')

    st.markdown('<div class="section-title">Brand Memory</div>', unsafe_allow_html=True)
    text = BRAND_MEMORY_PATH.read_text(encoding='utf-8') if BRAND_MEMORY_PATH.exists() else '{}'
    edited = st.text_area('Edit brand_memory.json', text, height=300)
    if st.button('Save Brand Memory'):
        try:
            json.loads(edited)
            BRAND_MEMORY_PATH.write_text(edited, encoding='utf-8')
            st.success('Brand memory saved.')
        except Exception as e:
            st.error(f'Invalid JSON: {e}')
