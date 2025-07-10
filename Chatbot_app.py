import streamlit as st
import requests

# 🚨 Debug line to confirm you're using the right version
st.warning("✅ THIS IS THE UPDATED VERSION")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
st.write("Using Model URL:", API_URL)

# Load secret
try:
    huggingface_token = st.secrets["api"]["huggingface_token"]
    headers = {"Authorization": f"Bearer {huggingface_token}"}
except KeyError:
    st.error("❌ Hugging Face token missing in .streamlit/secrets.toml")
    st.stop()

def query_huggingface(prompt):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt}
        )
        st.code(f"🔍 Status Code: {response.status_code}")
        st.code(f"📦 Raw Response: {response.text}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_response(prompt):
    output = query_huggingface(prompt)
    if "error" in output:
        return "❌ Error: " + output["error"]
    try:
        return output[0]["generated_text"]
    except Exception:
        return "⚠️ Unexpected response structure."

st.title("🤖 Simple HuggingFace Chatbot")
prompt = st.text_area("Your message", height=150)

if st.button("Send"):
    if not prompt.strip():
        st.warning("Please enter a message.")
    else:
        with st.spinner("Thinking..."):
            response = get_response(prompt)
        st.success("Response:")
        st.write(response)
