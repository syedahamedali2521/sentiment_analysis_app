import streamlit as st
import pandas as pd
import os, sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / 'src'))

from analyze_sentiment import predict_text, predict_batch

st.set_page_config(page_title='Neon Sentiment', layout='wide', page_icon='🧠')

# load css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css(os.path.join('app','static','style.css'))

st.markdown('<div class="header"><h1 class="title">NEON <span style="color:#b400ff">SENTI</span></h1><p class="sub">Futuristic Sentiment Analysis — DistilBERT (online)</p></div>', unsafe_allow_html=True)
st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1,2], gap='large')
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('### 🔎 Analyze Text or Upload CSV', unsafe_allow_html=True)
    text_input = st.text_area('Enter text to analyze', height=150)
    uploaded = st.file_uploader('Or upload a CSV (with a "text" column)', type=['csv'])
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    if st.button('Analyze', key='single', help='Analyze the input text or uploaded CSV'):
        if uploaded is not None:
            try:
                df = pd.read_csv(uploaded)
                if 'text' not in df.columns:
                    st.error('CSV must have a column named "text".')
                else:
                    st.session_state['bulk'] = df['text'].tolist()
                    st.session_state['bulk_results'] = None
                    st.experimental_rerun()
            except Exception as e:
                st.error(f'Failed to read CSV: {e}')
        elif text_input.strip() == '':
            st.warning('Please enter text or upload a CSV.')
        else:
            st.session_state['single_text'] = text_input.strip()
            st.session_state['single_result'] = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('### ⚙️ Options', unsafe_allow_html=True)
    model_info = st.checkbox('Show model info (will display HF model id)', value=True)
    show_conf = st.checkbox('Show confidence score', value=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('### 🧠 Results', unsafe_allow_html=True)
    if 'single_text' in st.session_state and st.session_state['single_text']:
        txt = st.session_state['single_text']
        st.markdown(f'**Input:** {txt}')
        with st.spinner('Analyzing...'):
            try:
                res = predict_text(txt)
            except Exception as e:
                st.error(f'Error loading model or predicting: {e}')
                st.stop()
        label = res['label']
        score = res['score']
        st.markdown(f'**Sentiment:** {label}  {"- " + str(round(score,3)) if show_conf else ""}')
        # glowing bars
        pos = score if label=='Positive' else 0.0
        neg = score if label=='Negative' else 0.0
        neu = 1.0 - (pos+neg)
        # render bars
        def render_bar(name, value, color_hex):
            width = int(value*100)
            st.markdown(f"<div class='label'>{name} — {round(value,3)}</div>" , unsafe_allow_html=True)
            st.markdown(f"<div class='glow-bar'><div class='glow-fill' style='width:{width}%; background:{color_hex};'></div></div>", unsafe_allow_html=True)
        render_bar('Positive', pos, 'linear-gradient(90deg,#00ff88,#00ffd0)')
        render_bar('Neutral', neu, '#00e5ff')
        render_bar('Negative', neg, 'linear-gradient(90deg,#ff3b3b,#ff8b8b)')
    elif 'bulk' in st.session_state and st.session_state['bulk']:
        texts = st.session_state['bulk']
        st.markdown(f'Processing **{len(texts)}** texts...')
        with st.spinner('Analyzing batch...'):
            try:
                results = predict_batch(texts)
            except Exception as e:
                st.error(f'Error loading model or predicting: {e}')
                st.stop()
        # show first results
        for r in results[:50]:
            st.markdown('<div style="margin-bottom:8px">', unsafe_allow_html=True)
            st.markdown(f"<div class='label'>{r['label']} — {round(r['score'],3)}</div>", unsafe_allow_html=True)
            width = int(r['score']*100)
            color = 'linear-gradient(90deg,#00ff88,#00ffd0)' if r['label']=='Positive' else 'linear-gradient(90deg,#ff3b3b,#ff8b8b)'
            st.markdown(f"<div class='glow-bar'><div class='glow-fill' style='width:{width}%; background:{color};'></div></div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('No results yet — enter text or upload a CSV and click **Analyze**.', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
# --- FOOTER ---

st.markdown('<div style="text-align:center; color:rgba(200,230,255,0.5)">Made by ❤️ Syed Ahamed Ali</div>', unsafe_allow_html=True)
