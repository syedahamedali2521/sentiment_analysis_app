import streamlit as st
import pandas as pd
import os, sys
from pathlib import Path

# -------------------------------
# ✅ Import setup for Streamlit Cloud
# -------------------------------
project_root = Path(__file__).resolve().parents[1]
src_path = project_root / "src"

if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from analyze_sentiment import predict_text, predict_batch
except Exception as e:
    st.error(f"❌ Import failed: {e}")
    st.stop()

# -------------------------------
# 🧠 Page Config
# -------------------------------
st.set_page_config(page_title="Neon Sentiment", layout="wide", page_icon="🧠")

# -------------------------------
# 💅 Load Neon CSS
# -------------------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = Path(__file__).parent / "static" / "style.css"
local_css(css_path)


# -------------------------------
# 🌌 Header
# -------------------------------
st.markdown(
    """
    <div class="header">
        <h1 class="title">NEON <span style="color:#b400ff">SENTI</span></h1>
        <p class="sub">Futuristic Sentiment Analysis — DistilBERT (Online Model)</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

# -------------------------------
# 🔍 Input Section
# -------------------------------
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔎 Analyze Text or Upload CSV", unsafe_allow_html=True)

    text_input = st.text_area("Enter text to analyze", height=150)
    uploaded = st.file_uploader("Or upload a CSV (with a 'text' column)", type=["csv"])
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    if st.button("Analyze", key="analyze", help="Analyze text or uploaded CSV"):
        if uploaded is not None:
            try:
                df = pd.read_csv(uploaded)
                if "text" not in df.columns:
                    st.error("CSV must have a column named 'text'.")
                else:
                    st.session_state["bulk"] = df["text"].tolist()
                    st.session_state["bulk_results"] = None
                    st.rerun()  # ✅ use new API
            except Exception as e:
                st.error(f"Failed to read CSV: {e}")
        elif not text_input.strip():
            st.warning("⚠️ Please enter text or upload a CSV.")
        else:
            st.session_state["single_text"] = text_input.strip()
            st.session_state["single_result"] = None
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Options", unsafe_allow_html=True)
    show_conf = st.checkbox("Show confidence score", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# 🧠 Results Section
# -------------------------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Results", unsafe_allow_html=True)

    if "single_text" in st.session_state and st.session_state["single_text"]:
        txt = st.session_state["single_text"]
        st.markdown(f"**Input:** {txt}")
        with st.spinner("Analyzing... 🚀"):
            try:
                res = predict_text(txt)
            except Exception as e:
                st.error(f"Error loading model or predicting: {e}")
                st.stop()

        label = res["label"].upper()
        score = res["score"]

        glow_color = {
            "POSITIVE": "linear-gradient(90deg,#00ff88,#00ffd0)",
            "NEGATIVE": "linear-gradient(90deg,#ff3b3b,#ff8b8b)",
            "NEUTRAL": "#00e5ff",
        }.get(label, "#00e5ff")

        emoji = {"POSITIVE": "🟢", "NEGATIVE": "🔴", "NEUTRAL": "🔵"}.get(label, "🔵")

        st.markdown(
            f"""
            <div class="result-box" style="border:2px solid {glow_color.split(',')[1][:-1]}; box-shadow:0 0 20px {glow_color.split(',')[1][:-1]}">
                {emoji} Sentiment: <b>{label}</b><br>
                Confidence: {score:.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif "bulk" in st.session_state and st.session_state["bulk"]:
        texts = st.session_state["bulk"]
        st.markdown(f"Processing **{len(texts)}** texts...")
        with st.spinner("Analyzing batch..."):
            try:
                results = predict_batch(texts)
            except Exception as e:
                st.error(f"Error loading model or predicting: {e}")
                st.stop()

        for r in results[:50]:
            label = r["label"].upper()
            score = r["score"]
            glow_color = (
                "linear-gradient(90deg,#00ff88,#00ffd0)"
                if label == "POSITIVE"
                else "linear-gradient(90deg,#ff3b3b,#ff8b8b)"
                if label == "NEGATIVE"
                else "#00e5ff"
            )
            st.markdown(
                f"""
                <div class='label'>{label} — {round(score, 3)}</div>
                <div class='glow-bar'>
                    <div class='glow-fill' style='width:{int(score*100)}%; background:{glow_color};'></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "No results yet — enter text or upload a CSV and click **Analyze**.",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# 💬 Footer
# -------------------------------
st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center; color:rgba(200,230,255,0.5)">Made with ❤️ by Syed Ahamed Ali</div>',
    unsafe_allow_html=True,
)

