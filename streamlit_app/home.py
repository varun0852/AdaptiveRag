import streamlit as st
import uuid

st.set_page_config(
    page_title="Adaptive RAG",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Adaptive RAG Chatbot")
st.markdown("Smart chatbot that routes questions to documents, general knowledge, or live web search.")

st.divider()

if "session_id" not in st.session_state:
    st.session_state.session_id = None

username = st.text_input("Enter your name to start:", placeholder="e.g. Varun")

if st.button("Start Chatting", type="primary"):
    if username.strip():
        st.session_state.session_id = f"{username.strip()}_{uuid.uuid4().hex[:8]}"
        st.session_state.username = username.strip()
        st.switch_page("pages/chat.py")
    else:
        st.error("Please enter your name.")

st.divider()
st.caption("Powered by Groq (Llama 3.3 70B) · LangGraph · Qdrant · Tavily")