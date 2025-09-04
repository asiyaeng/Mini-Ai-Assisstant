import streamlit as st
import requests
import os

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="Mini AI Assistant", page_icon="🤖")
st.title("🤖 Mini AI Assistant")
st.write("Ask me anything, and I'll try to answer using Hugging Face's flan-t5-base model!")

# -------------------------
# Hugging Face API Setup
# -------------------------
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HF_TOKEN = os.getenv("HF_TOKEN")  # stored in Streamlit Cloud Secrets
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def query(payload):
    """Send query to Hugging Face API"""
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# -------------------------
# User Input
# -------------------------
user_input = st.text_input("💬 Enter your question:")

if user_input:
    if not HF_TOKEN:
        st.error("❌ Hugging Face token not found! Please set `HF_TOKEN` in Streamlit Secrets.")
    else:
        with st.spinner("🤔 Thinking..."):
            output = query({"inputs": user_input})

            if "error" in output:
                st.error(f"⚠️ API Error: {output['error']}")
            else:
                try:
                    st.success(output[0]["generated_text"])
                except:
                    st.warning("⚠️ Could not parse response. Try again.")
