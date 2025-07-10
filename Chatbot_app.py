import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="AI Companion", page_icon="🤖")

# Title
st.title("🤖 AI Companion Chatbot")
st.caption("An emotionally intelligent chatbot powered by Nous Hermes 2")

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
headers = {"Authorization": f"Bearer {st.secrets['api']['huggingface_token']}"}

# Query function
def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Format chat history
def build_prompt(history, user_input):
    prompt = ""
    for msg in history[-4:]:  # Last 2 rounds
        prompt += f"User: {msg['user']}\nAI: {msg['ai']}\n"
    prompt += f"User: {user_input}\nAI:"
    return prompt

# Generate response
def get_response(prompt):
    output = query_huggingface({
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 150,
            "return_full_text": False
        }
    })
    try:
        return output[0]["generated_text"]
    except (KeyError, IndexError, TypeError):
        return "I'm having trouble thinking right now. Try again in a moment."

# Session state to store conversation
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", key="input")

if user_input:
    with st.spinner("Thinking..."):
        prompt = build_prompt(st.session_state.history, user_input)
        ai_reply = get_response(prompt)

    st.session_state.history.append({"user": user_input, "ai": ai_reply})

# Display chat history
for turn in st.session_state.history:
    st.markdown(f"**You**: {turn['user']}")
    st.markdown(f"**AI**: {turn['ai']}")

# Clear history button
if st.button("🗑️ Clear Chat"):
    st.session_state.history = []
