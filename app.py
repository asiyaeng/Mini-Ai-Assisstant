import streamlit as st
from transformers import pipeline

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="Mini AI Assistant", page_icon="🤖")
st.title("🤖 Mini AI Assistant")
st.write("Ask me anything! Powered by open-source model google/flan-t5-small.")

# -------------------------
# Load Model (once at startup)
# -------------------------
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

generator = load_model()

# -------------------------
# User Input
# -------------------------
user_input = st.text_input("💬 Enter your question:")

if user_input:
    with st.spinner("🤔 Thinking..."):
        # Add a task prefix so model understands
        prompt = f"Explain in simple words: {user_input}"
        result = generator(prompt, max_length=200, num_return_sequences=1)
        st.success(result[0]["generated_text"])


