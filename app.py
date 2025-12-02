import base64
from pathlib import Path

import numpy as np
import streamlit as st

CORRECT_ANSWER = "an agreed scope and no change requests"

st.set_page_config(page_title="Advisory Christmas", page_icon="🎄", layout="centered")


def set_background(png_file: str) -> None:
    file_path = Path(png_file)
    with open(file_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #111827;
    }}
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stTextInput > label {{
        color: #111827 !important;
    }}
    .santa-frame img {{
        border-radius: 18px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
        border: 3px solid rgba(15, 23, 42, 0.7);
    }}
    .tagline {{
        font-size: 0.95rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }}
    .hint {{
        font-size: 0.8rem;
        opacity: 0.85;
        margin-top: 0.5rem;
    }}
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
        color: #111827 !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def extract_features(text: str) -> dict:
    t = text.lower().strip()
    words = t.split() if t else []
    length = len(words)

    buzzwords = [
        "scope", "roadmap", "operating model", "change request",
        "digital", "data", "ai", "ml", "analytics", "resilience",
        "vegetation", "risk", "grid",
    ]
    fun_words = ["bonus", "holiday", "bike", "ps5", "champagne", "apres", "après"]

    buzz_count = sum(1 for b in buzzwords if b in t)
    fun_count = sum(1 for f in fun_words if f in t)
    avg_word_len = np.mean([len(w) for w in words]) if words else 0.0

    return {
        "length": length,
        "buzz_count": buzz_count,
        "fun_count": fun_count,
        "avg_word_len": avg_word_len,
    }


def ml_score(features: dict) -> float:
    x = np.array(
        [
            1.0,
            features["length"],
            features["buzz_count"],
            features["fun_count"],
            features["avg_word_len"],
        ]
    )
    w = np.array([-2.0, -0.08, 0.9, -1.1, 0.4])
    z = float(np.dot(w, x))
    prob = 1.0 / (1.0 + np.exp(-z))
    return round(prob * 100, 1)


# ---------- State ----------
if "last_result" not in st.session_state:
    st.session_state.last_result = None

res = st.session_state.last_result

# Background from latest result
if res and res["approved"]:
    background_image = "Apres.png"
else:
    background_image = "Snow.png"

set_background(background_image)

# ---------- Top content & photo ----------
st.title("Happy Christmas Advisory 🎄")
st.markdown(
    "<p class='tagline'>Buro Happold | Advisory AI‑assisted Christmas scoping.</p>",
    unsafe_allow_html=True,
)

st.write(
    "Santa has been seconded into the Advisory team this year. "
    "He’s brought an AI model that scores how deliverable your wish really is."
)

base_path = Path(__file__).parent

# Santa image based on latest result
if res and res["approved"]:
    image_path = base_path / "santa_thumbs_up.png"
    caption = "Santa approves the business case – see you at après! 🎁"
else:
    image_path = base_path / "santa_ok.png"
    caption = "Santa (Advisory Edition) – calmly reviewing your scope."

st.markdown('<div class="santa-frame">', unsafe_allow_html=True)
st.image(str(image_path), caption=caption, width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Input section (under the photo) ----------
st.subheader("What would you like for Christmas (Advisory edition)?")

wish = st.text_input(
    "Type your wish here:",
    placeholder="e.g. An agreed scope and no change requests",
)

st.markdown(
    "<p class='hint'>Hint: the AI likes clear scope, roadmaps and funding more than bikes and bonuses.</p>",
    unsafe_allow_html=True,
)

clicked = st.button("Ask Santa & the AI model")

if clicked:
    feats = extract_features(wish)
    score = ml_score(feats)
    approved = wish.strip().lower() == CORRECT_ANSWER

    santa_msg = (
        "Approved. Let's deliver – then go to après."
        if approved
        else "👎 Santa thinks that's out of scope. The AI model agrees… mostly."
    )

    st.session_state.last_result = {
        "approved": approved,
        "message": santa_msg,
        "features": feats,
        "score": score,
    }
    res = st.session_state.last_result  # use new result immediately

# ---------- Results section ----------
if res:
    msg = res["message"]
    feats = res["features"]
    score = res["score"]

    if score >= 70:
        st.success(msg)
    elif score >= 40:
        st.warning(msg)
    else:
        st.error(msg)

    st.subheader("🤖 Advisory AI feasibility analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Feasibility score", f"{score} / 100")
        st.write(f"- Words: **{feats['length']}**")
        st.write(f"- Buzzwords: **{feats['buzz_count']}**")
    with col2:
        st.write(f"- Fun words: **{feats['fun_count']}**")
        st.write(f"- Avg. word length: **{feats['avg_word_len']:.1f}**")
        if score >= 70:
            st.success("Model verdict: High likelihood of Advisory delivery.")
        elif score >= 40:
            st.warning("Model verdict: Borderline – expect a few governance boards.")
        else:
            st.info("Model verdict: Ambitious. Recommend a different approach.")
