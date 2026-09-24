# LLM Token Visualizer

A **Streamlit** app that shows how different LLM tokenizers split the same text into tokens. Each token is rendered in its own colour with a token count, so you can compare models side by side.

## Why it matters
Tokenization decides an LLM's **cost** (APIs bill per token), how much fits in the **context window**, and some of its **behaviour** (e.g. why models struggle to count letters or do arithmetic on long numbers). This app makes those differences visible:
- BERT's **WordPiece** (`play ##ing`) vs. GPT-2's **byte-level BPE** (`Ġplaying`)
- how code-focused tokenizers (StarCoder2) handle indentation and symbols
- how many tokens the same sentence costs in each model — often very different for non-English text

## Supported tokenizers
| Model | Hugging Face id | Tokenizer type |
|---|---|---|
| BERT | `bert-base-cased` | WordPiece |
| GPT-2 | `gpt2` | byte-level BPE |
| GPT-4 | `Xenova/gpt-4` | BPE (cl100k_base) |
| Flan-T5 | `google/flan-t5-small` | SentencePiece (Unigram) |
| StarCoder2 | `bigcode/starcoder2-15b` | BPE for code |
| Phi-3 | `microsoft/Phi-3-mini-4k-instruct` | SentencePiece BPE |
| Qwen2-VL | `Qwen/Qwen2-VL-7B-Instruct` | byte-level BPE |
| DeepSeek-R1 | `deepseek-ai/DeepSeek-R1-0528` | byte-level BPE |

Only the tokenizer files are downloaded (a few MB each), never the model weights.

## How it works
1. `AutoTokenizer.from_pretrained()` loads the selected tokenizer; `@st.cache_resource` keeps it in memory, so switching back is instant.
2. The text is encoded to token ids; each id is decoded back to its text piece.
3. Pieces are rendered as coloured HTML spans with the total token count; tokenizers that fail to load show a friendly error instead of crashing the app.

## Project structure
```
llm-token-visualizer/
├── app.py            # Streamlit UI + tokenization / rendering logic
├── requirements.txt  # streamlit, transformers
└── README.md
```

## Run locally
```bash
git clone https://github.com/kishorhange111/llm-token-visualizer.git
cd llm-token-visualizer
pip install -r requirements.txt
streamlit run app.py
```
Deploys as-is to **Streamlit Community Cloud** (main file: `app.py`).

## Tech stack
Python · Streamlit · Hugging Face Transformers (`AutoTokenizer`)
