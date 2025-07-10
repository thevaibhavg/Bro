import streamlit as st
import requests

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")
st.markdown("Talk to an AI powered by Hugging Face.")

# --- API CONFIG ---
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"  # ✅ verified model

try:
    huggingface_token = st.secrets["api"]["huggingface_token"]
    headers = {"Authorization": f"Bearer {huggingface_token}"}
except KeyError:
    st.error("🔐 Hugging Face token not found in secrets!")
    st.stop()

# --- QUERY FUNCTION ---
def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        # Debug info
        st.code(f"STATUS: {response.status_code}")
        st.code(f"RAW RESPONSE: {response.text}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {e}")
        return {"error": str(e)}

# --- RESPONSE PARSER ---
def get_response(prompt):
    output = query_huggingface(prompt)
    if "error" in output:
        return "Sorry, the AI couldn't respond properly."

    try:
        return output[0]["generated_text"]
    except (KeyError, IndexError, TypeError):
        return "Model did not return expected output."

# --- UI ---
prompt = st.text_area("💬 Your message", placeholder="Type your question here...")

if st.button("Send"):
    if not prompt.strip():
        st.warning("Please enter a message.")
    else:
        with st.spinner("Thinking..."):
            response = get_response(prompt)
        st.success("🧠 AI Response:")
        st.write(response)
