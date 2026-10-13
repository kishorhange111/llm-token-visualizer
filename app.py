"""
LLM Token Visualizer - a Streamlit app that shows how different LLM tokenizers
split the same text.

Pick a model, type some text, and every token is drawn in its own colour with
the total token count. The tokenization and rendering logic lives in the
token_visualizer/ package (unit-tested); this file is only the UI.

Run:  streamlit run app.py
"""
import streamlit as st
from transformers import AutoTokenizer

from token_visualizer import MODELS, render_tokens_html, tokenize


@st.cache_resource
def load_tokenizer(name: str):
    """Load a tokenizer from the Hugging Face Hub once per server, instead of on every click.

    st.cache_resource keeps the object in memory across reruns and users, so
    switching back to a model that was already used is instant.

    Args:
        name: Hugging Face Hub id, e.g. "gpt2".

    Returns:
        The loaded tokenizer.
    """
    return AutoTokenizer.from_pretrained(name)


def show_tokens(sentence: str, tokenizer_name: str):
    """Tokenize a sentence with the chosen tokenizer.

    Args:
        sentence: the text to tokenize.
        tokenizer_name: Hugging Face Hub id of the tokenizer.

    Returns:
        (html, count): the tokens as coloured HTML spans, and the number of tokens.
    """
    tokenizer = load_tokenizer(tokenizer_name)
    pieces = tokenize(tokenizer, sentence)
    return render_tokens_html(pieces), len(pieces)


# --- UI ----------------------------------------------------------------------
# Streamlit re-runs this whole script top to bottom on every interaction.
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
            # unsafe_allow_html is needed for the coloured spans.
            st.markdown(f"<p>{html}</p>", unsafe_allow_html=True)
            st.caption(f"Token count: {count}")
        except Exception as e:
            # Some tokenizers fail to load (gated repo, network, missing extra package);
            # show the reason instead of crashing the whole app.
            st.error(f"Could not load the {selected_option} tokenizer: {e}")
    else:
        st.warning("Please enter text and select a model before processing.")
