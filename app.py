import streamlit as st
from transformers import AutoTokenizer

MODELS = {
    "BERT": "bert-base-cased",
    "GPT-2": "gpt2",
    "GPT-4": "Xenova/gpt-4",
    "Flan-T5-small": "google/flan-t5-small",
    "StarCoder2-15B": "bigcode/starcoder2-15b",
    "Phi-3": "microsoft/Phi-3-mini-4k-instruct",
    "Qwen2 - Vision-Language Model": "Qwen/Qwen2-VL-7B-Instruct",
    "DeepSeek-R1-0528": "deepseek-ai/DeepSeek-R1-0528",
}

COLORS = ["#FF5733", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6"]


@st.cache_resource
def load_tokenizer(name: str):
    """Load each tokenizer only once, instead of on every click."""
    return AutoTokenizer.from_pretrained(name)


def show_tokens(sentence: str, tokenizer_name: str):
    """Return the tokens as HTML, each in a different colour, plus the token count."""
    tokenizer = load_tokenizer(tokenizer_name)
    token_ids = tokenizer(sentence).input_ids
    colored_text = ""
    for idx, t in enumerate(token_ids):
        colored_text += (
            f'<span style="color: {COLORS[idx % len(COLORS)]}; font-weight: bold;">'
            f"{tokenizer.decode(t)}</span> "
        )
    return colored_text, len(token_ids)


st.set_page_config(page_title="Token Visualizer", page_icon="🚀", layout="wide")
st.title("Token Visualizer")

text = st.text_area("Text", placeholder="Type your text here...")
st.header("Choose a model from the dropdown")
selected_option = st.selectbox("Select a Model:", list(MODELS.keys()))

if st.button("Process Data"):
    if text and selected_option:
        st.subheader("Text:")
        st.write(text)
        st.subheader("Selected Model:")
        st.write(f"**{selected_option}**")
        try:
            html, count = show_tokens(text, MODELS[selected_option])
            st.markdown(f"<p>{html}</p>", unsafe_allow_html=True)
            st.caption(f"Token count: {count}")
        except Exception as e:
            st.error(f"Could not load the {selected_option} tokenizer: {e}")
    else:
        st.warning("Please enter text and select a model before processing.")
