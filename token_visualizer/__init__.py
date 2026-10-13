"""
token_visualizer: the tokenization and rendering logic behind the Streamlit app.

app.py is only the user interface. Everything it shows - the list of
supported tokenizers, how text becomes token pieces, and how those pieces are
turned into coloured HTML - lives here, so it can be unit-tested with a fake
tokenizer and without Streamlit or any download.
"""
from .core import COLORS, MODELS, render_tokens_html, tokenize

__all__ = ["COLORS", "MODELS", "render_tokens_html", "tokenize"]
