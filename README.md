# LLM Token Visualizer

A **Streamlit** app that shows how different LLM tokenizers split the same text into tokens. Each token is shown in its own colour, so you can compare models side by side.

## Why it's useful
Tokenization affects an LLM's cost, context length and behaviour. This app makes it easy to see, for example:
- how BERT's WordPiece splits words differently from GPT-2's byte-level BPE
- how code-focused tokenizers (StarCoder2) handle source code
- how many tokens the same sentence costs in different models

## Supported tokenizers
BERT · GPT-2 · GPT-4 · Flan-T5 · StarCoder2 · Phi-3 · Qwen2-VL · DeepSeek-R1

## Tech
Python · Streamlit · Hugging Face Transformers (`AutoTokenizer`)

## Run it locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
