import streamlit as st
from transformers import pipeline
import nltk
from nltk.corpus import wordnet

# Download WordNet data (only first run)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="Mini AI Assistant", page_icon="🤖")
st.title("🤖 Mini AI Assistant")
st.write("Ask me anything! Powered by open-source model google/flan-t5-base + WordNet dictionary fallback.")

# -------------------------
# Load Model (once at startup)
# -------------------------
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

generator = load_model()

# -------------------------
# WordNet Fallback
# -------------------------
def get_meaning(word: str):
    syns = wordnet.synsets(word)
    if syns:
        return syns[0].definition()
    return None

# -------------------------
# Smart Prompt Engineering
# -------------------------
def build_prompt(user_input: str) -> str:
    text = user_input.lower()

    if "meaning" in text or "define" in text:
        return f"Define in simple words: {user_input}"
    elif "who is" in text:
        return f"Answer briefly: {user_input}"
    elif "translate" in text:
        return f"{user_input}"
    elif "summarize" in text or "summary" in text:
        return f"Summarize this: {user_input}"
    else:
        return f"Explain clearly: {user_input}"

# -------------------------
# User Input
# -------------------------
user_input = st.text_input("💬 Enter your question:")

if user_input:
    with st.spinner("🤔 Thinking..."):
        # WordNet fallback for "meaning of X"
        if "meaning of" in user_input.lower() or "define" in user_input.lower():
            # Try to extract single word after "meaning of"
            word = user_input.lower().replace("what is the meaning of", "").replace("meaning of", "").replace("define", "").strip()
            meaning = get_meaning(word)
            if meaning:
                st.success(f"📖 Dictionary meaning of **{word}**: {meaning}")
            else:
                # If WordNet fails, fall back to model
                prompt = build_prompt(user_input)
                result = generator(prompt, max_length=200, num_return_sequences=1)
                st.success(result[0]["generated_text"])
        else:
            # General case → use model
            prompt = build_prompt(user_input)
            result = generator(prompt, max_length=200, num_return_sequences=1)
            st.success(result[0]["generated_text"])

