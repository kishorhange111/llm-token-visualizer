import streamlit as st
from transformers import AutoTokenizer

colors = [
    '102;194;165', '252;141;98', '141;160;203',
    '231;138;195', '166;216;84', '255;217;47'
]

def show_tokens(sentence: str, tokenizer_name: str):
    """ return the tokens each separated by a different color """

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    token_ids = tokenizer(sentence).input_ids
    colors = ["#FF5733", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6"]
    colored_text = ""
    for idx, t in enumerate(token_ids):
        colored_text += f'<span style="color: {colors[idx % len(colors)]}; font-weight: bold;">{tokenizer.decode(t)}</span> '
    
    return colored_text

st.set_page_config(
    page_title="Token Visualizer",
    page_icon="🚀",  
    layout="wide" 
)

st.title("Token Visualizer ")

text = st.text_area("", placeholder="Type your text here...")
st.header("Choose a model from the dropdown")

options = ["BERT","GPT-2","GPT-4","Flan-T5-small","StarCoder2-15B","Phi-3","Qwen2 - Vision-Language Model","DeepSeek-R1-0528","Llama-3.1-8B-Instruct","Llama-4-Scout-17B-16E-Instruct"]
selected_option = st.selectbox("Select a Model:", options)

if st.button("Process Data"):
    if text and selected_option:
        st.subheader("Text :")
        st.write(text)

        st.subheader("Selected Model:")
        st.write(f"**{selected_option}**")

        if selected_option == "BERT":
            st.markdown(f"<p>{show_tokens(text, 'bert-base-cased')}</p>", unsafe_allow_html=True)
        elif selected_option == "GPT-2":
            st.markdown(f"<p>{show_tokens(text, 'gpt2')}</p>", unsafe_allow_html=True)
        elif selected_option == "GPT-4":
            st.markdown(f"<p>{show_tokens(text, 'Xenova/gpt-4')}</p>", unsafe_allow_html=True)
        elif selected_option == "Flan-T5-small":
            st.markdown(f"<p>{show_tokens(text, 'google/flan-t5-small')}</p>", unsafe_allow_html=True)
        elif selected_option == "StarCoder2-15B":
            st.markdown(f"<p>{show_tokens(text, 'bigcode/starcoder2-15b')}</p>", unsafe_allow_html=True)
        elif selected_option == "Phi-3":
            st.markdown(f"<p>{show_tokens(text, 'microsoft/Phi-3-mini-4k-instruct')}</p>", unsafe_allow_html=True)
        elif selected_option == "Qwen2 - Vision-Language Model":
            st.markdown(f"<p>{show_tokens(text, 'Qwen/Qwen2-VL-7B-Instruct')}</p>", unsafe_allow_html=True)
        elif selected_option == "DeepSeek-R1-0528":
            st.markdown(f"<p>{show_tokens(text, 'deepseek-ai/DeepSeek-R1-0528')}</p>", unsafe_allow_html=True)
        elif selected_option == "Llama-3.1-8B-Instruct":
            st.markdown(f"<p>{show_tokens(text, 'meta-llama/Llama-3.1-8B-Instruct')}</p>", unsafe_allow_html=True)
        elif selected_option == "Llama-4-Scout-17B-16E-Instruct":
            st.markdown(f"<p>{show_tokens(text, 'meta-llama/Llama-4-Scout-17B-16E-Instruct')}</p>", unsafe_allow_html=True)
    else:
        st.warning("Please enter text and select a model before processing.")
