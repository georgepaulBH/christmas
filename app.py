import base64
from pathlib import Path

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
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# Full-page snowy background
set_background("Snow.png")  # Snow.png in same folder as app.py [web:70][web:72][web:76]

st.title("Happy Christmas Advisory 🎄")

st.markdown(
    "<p class='tagline'>Buro Happold – now taking Christmas requests.</p>",
    unsafe_allow_html=True,
)

st.write(
    "Santa has been seconded into the Advisory team this year. "
    "He’s happy to talk risk, resilience and roadmaps..."
)

# Track last status
if "last_status" not in st.session_state:
    st.session_state.last_status = "neutral"

base_path = Path(__file__).parent

# Image logic:
# - default & wrong answers: normal Santa
# - correct answer: thumbs-up Santa
if st.session_state.last_status == "approved":
    image_path = base_path / "santa_thumbs_up.png"
    caption = "Santa approves the business case – let’s deliver! 🎁"
else:
    image_path = base_path / "santa_ok.png"
    caption = "Santa (Advisory Edition) – calmly reviewing your scope."

st.markdown('<div class="santa-frame">', unsafe_allow_html=True)
st.image(str(image_path), caption=caption, width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

st.subheader("What would you like for Christmas (Advisory edition)?")

wish = st.text_input(
    "Type your wish here:",
    placeholder="e.g. 'a new bike' or 'a fully funded roadmap'",
)

st.markdown(
    "<p class='hint'>Hint: Santa works in Advisory now – he’s not bringing you a new bike, "
    "but he might bring a fully funded roadmap…</p>",
    unsafe_allow_html=True,
)

if st.button("Ask Santa"):
    if wish.strip().lower() == CORRECT_ANSWER:
        st.session_state.last_status = "approved"
        st.success("Approved. Let's deliver – on time, on budget, and in scope.")
    else:
        st.session_state.last_status = "neutral"
        st.error(
            "👎 No, that's out of scope. Please resubmit with a more Advisory‑appropriate ask "
            "(hint: think scope, change and funding, not bikes)."
        )
    st.rerun()
