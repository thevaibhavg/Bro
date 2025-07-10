import streamlit as st
import requests

# --- SETUP ---

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Replace with your model if needed

# Load token safely
try:
    huggingface_token = st.secrets["api"]["huggingface_token"]
    headers = {"Authorization": f"Bearer {huggingface_token}"}
except KeyError:
    st.error("🔐 Hugging Face token not found in secrets! Please check `.streamlit/secrets.toml` or Streamlit Cloud settings.")
    st.stop()

# --- FUNCTIONS ---

def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)

    # Debug info
    st.write("📡 Status Code:", response.status_code)
    st.write("🧾 Raw Response:", response.text)

    try:
        response.raise_for_status()  # Catch HTTP errors
        return response.json()
    except requests.exceptions.JSONDecodeError:
        st.error("❌ Failed to parse Hugging Face response as JSON.")
        return {"error": "Invalid response format"}
    except requests.exceptions.HTTPError as e:
        st.error(f"🚨 HTTP error from Hugging Face: {e}")
        return {"error": str(e)}

def get_response(prompt):
    output = query_huggingface({
        "inputs": prompt,
    })
    if "error" in output:
        return "Sorry, the AI couldn't respond properly."
    
    try:
        return output[0]["generated_text"]
    except (KeyError, IndexError, TypeError):
        return "The model didn't return expected output."

# --- UI ---

st.title("🤖 AI Chatbot")
st.markdown("Ask me anything!")

prompt = st.text_area("Your message", placeholder="Type your question here...", height=150)

if st.button("Send"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            ai_reply = get_response(prompt)
        st.success("AI Response:")
        st.write(ai_reply)
