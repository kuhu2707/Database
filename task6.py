
import os 
import streamlit as st
from transformers import pipeline

# ------- firebase ----
import firebase_admin 
from firebase_admin import credentials, firestore

SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_KEY_PATH")

if not firebase_admin._apps:
    if os.path.exists(SERVICE_ACCOUNT_PATH):
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        st.success("initialized")
    else:
        db = None 
        st.warning("firestore is not configured")
else:
    db = firestore.client()

# --- Save messages to Firestore ---
def save_message(role, content):
    """Save chat message to Firestore."""
    if db:
        try:
            db.collection("chat_logs").add({
                "role": role,
                "content": content,
                "session_id": st.session_state.get("session_id", "default"),
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            st.error(f"Firestore error: {e}")


st.title("Chatbot")

@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

chatbot = load_model()

if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input("Ask me anything...")

if prompt:
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message("user", prompt)   

    result = chatbot(prompt, max_new_tokens=200)
    reply = result[0]["generated_text"].strip()

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    save_message("assistant", reply)   
