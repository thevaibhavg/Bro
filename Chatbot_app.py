import streamlit as st
import requests

# --- STREAMLIT SETUP ---
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")
st.markdown("Ask me anything and I'll try to respond like a helpful, intelligent companion.")

# --- HUGGING FACE API SETUP ---

# Use a working public instruct model (better for chat)
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
# Load token from Streamlit secrets
try:
    huggingface_token = st.secrets["api"]["huggingface_token"]
    headers = {"Authorization": f"Bearer {huggingface_token}"}
except KeyError:
    st.error("🔐 Hugging Face token not found in secrets! Add it to `.streamlit/secrets.toml` or Streamlit Cloud.")
    st.stop()

# --- QUERY FUNCTION ---

def query_huggingface(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        st.write("📡 Status Code:", response.status_code)
        st.write("🧾 Raw Response:", response.text)
        response.raise_for_status()  # Raise error for 4xx/5xx
        return response.json()
    except requests.exceptions.JSONDecodeError:
        st.error("❌ Failed to parse Hugging Face response as JSON.")
        return {"error": "Invalid response format"}
    except requests.exceptions.HTTPError as e:
        st.error(f"🚨 HTTP error from Hugging Face: {e}")
        return {"error": str(e)}
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")
        return {"error": str(e)}

# --- RESPONSE HANDLER ---

def get_response(prompt):
    output = query_huggingface({
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 200,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
        }
    })

    if "error" in output:
        return "Sorry, the AI couldn't respond properly."

    try:
        return output[0]["generated_text"]
    except (KeyError, IndexError, TypeError):
        return "The model didn't return expected output."

# --- UI INPUT/OUTPUT ---

prompt = st.text_area("💬 Your Message", placeholder="What’s on your mind?", height=150)

if st.button("Send"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            ai_reply = get_response(prompt)
        st.success("🧠 AI Response:")
        st.write(ai_reply)
