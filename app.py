import streamlit as st
import requests
import os

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="Mini AI Assistant", page_icon="🤖")
st.title("🤖 Mini AI Assistant")
st.write("Ask me anything and I'll try to answer!")

# -------------------------
# Hugging Face API Setup
# -------------------------
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HF_TOKEN = os.getenv("HF_TOKEN")  # stored securely in Streamlit Cloud → Settings → Secrets
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def query(payload):
    """Send a query to Hugging Face API and return response"""
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# -------------------------
# User Interaction
# -------------------------
user_input = st.text_input("💬 Enter your question:")

if user_input:
    with st.spinner("🤔 Thinking..."):
        output = query({"inputs": user_input})

        if "error" in output:
            st.error(f"⚠️ API Error: {output['error']}")
        else:
            try:
                st.success(output[0]["generated_text"])
            except:
                st.warning("⚠️ Could not parse response. Try again.")
