"""
Turn text into the token pieces an LLM actually sees, and render them as HTML.

An LLM never reads characters or words; it reads integer *token ids*. A
tokenizer splits text into pieces from a fixed vocabulary (WordPiece for
BERT, byte-level BPE for GPT-2, SentencePiece for T5, ...) and maps each
piece to an id. Different tokenizers split the same text very differently,
which changes cost (APIs bill per token), how much fits in the context window,
and some model behaviour.

The pipeline used by the app:

    text --tokenizer(text).input_ids--> [id, id, ...]
         --tokenizer.decode(id) each--> ["piece", "piece", ...]
         --render_tokens_html-->        <span style="color: ...">piece</span> ...
"""

import html

# Display name -> Hugging Face Hub id. Only the tokenizer files are downloaded
# (a few MB each); AutoTokenizer never fetches the model weights.
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

# Token colours, cycled so neighbouring tokens always differ.
COLORS = ["#FF5733", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6"]


def tokenize(tokenizer, text):
    """Split text into token ids and the text piece each id stands for.

    Args:
        tokenizer: a Hugging Face tokenizer (anything whose call returns an
            object with `.input_ids` and that has `.decode(id)`).
        text: the input string.

    Returns:
        A list of (token_id, piece) tuples, in order. Special tokens the
        tokenizer adds (e.g. BERT's [CLS] and [SEP]) are included, because
        they count towards the context window too.
    """
    token_ids = tokenizer(text).input_ids
    # Decode one id at a time so each piece shows exactly where a token starts and ends.
    return [(t, tokenizer.decode(t)) for t in token_ids]


def render_tokens_html(pieces, colors=COLORS):
    """Render token pieces as coloured, bold HTML spans separated by spaces.

    Args:
        pieces: list of text pieces (or (token_id, piece) tuples from tokenize()).
        colors: CSS colours to cycle through, one per token.

    Returns:
        An HTML string. Pieces are HTML-escaped, so text such as "<b>" or
        "&amp;" is shown literally instead of being interpreted by the browser.
    """
    spans = []
    for idx, piece in enumerate(pieces):
        if isinstance(piece, tuple):  # accept tokenize() output directly
            piece = piece[1]
        spans.append(
            f'<span style="color: {colors[idx % len(colors)]}; font-weight: bold;">{html.escape(piece)}</span> '
        )
    return "".join(spans)
