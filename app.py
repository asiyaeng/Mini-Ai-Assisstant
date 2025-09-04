import streamlit as st
import requests
import os

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="Mini AI Assistant", page_icon="🤖")
st.title("🤖 Mini AI Assistant")
st.write("Ask me anything! If API is down, I'll switch to offline mode.")

# -------------------------
# Hugging Face API Setup
# -------------------------
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HF_TOKEN = os.getenv("HF_TOKEN")  # add in Streamlit Cloud secrets
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def query_api(payload):
    """Send a query to Hugging Face API and return response"""
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# -------------------------
# Offline Fallback
# -------------------------
offline_responses = {
    "hello": "👋 Hi there! How can I help you today?",
    "who are you": "🤖 I am your Mini AI Assistant, built with Streamlit.",
    "bye": "👋 Goodbye! Have a great day!",
    "help": "💡 You can ask me general questions, or just say hello!",
}

def offline_answer(text):
    return offline_responses.get(text.lower(), "🤔 I don’t know that yet, but I’m learning!")

# -------------------------
# User Interaction
# -------------------------
user_input = st.text_input("💬 Enter your question:")

if user_input:
    # Try API first
    if HF_TOKEN:
        with st.spinner("🤔 Thinking... (API Mode)"):
            output = query_api({"inputs": user_input})

            if "error" in output:
                st.warning(f"⚠️ API failed: {output['error']}. Switching to offline mode...")
                st.success(offline_answer(user_input))
            else:
                try:
                    st.success(output[0]["generated_text"])
                except:
                    st.warning("⚠️ Could not parse API response. Switching to offline mode...")
                    st.success(offline_answer(user_input))
    else:
        st.info("🔌 No API token found. Running in Offline Mode.")
        st.success(offline_answer(user_input))
