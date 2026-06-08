import streamlit as st
import requests
import os

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

# ✅ Points to Railway backend — update this after Railway deployment
API_BASE = os.getenv("API_BASE_URL", "https://YOUR-RAILWAY-URL.up.railway.app/rag")

if "session_id" not in st.session_state or not st.session_state.session_id:
    st.warning("Please go back to the home page and enter your name.")
    st.stop()

session_id = st.session_state.session_id
username = st.session_state.get("username", "User")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📄 Upload Documents")
    st.caption("Upload PDFs or TXT files to chat with them.")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])
    description = st.text_input("Document description", placeholder="e.g. Company HR policy")

    if st.button("Upload & Index", type="primary"):
        if uploaded_file and description.strip():
            with st.spinner("Indexing document..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/documents/upload",
                        headers={"x-description": description},
                        files={"file": (uploaded_file.name, uploaded_file.getvalue())}
                    )
                    if response.status_code == 200:
                        st.success(f"✅ '{uploaded_file.name}' indexed!")
                    else:
                        st.error(f"Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.warning("Please select a file and add a description.")

    st.divider()
    st.markdown(f"**Session:** `{session_id[:20]}...`")
    st.markdown("**Routes:** 📚 Index · 🧠 General · 🌐 Web Search")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title(f"💬 Chat — Hello, {username}!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_BASE}/query",
                    json={"query": user_input, "session_id": session_id},
                    timeout=60
                )
                if response.status_code == 200:
                    answer = response.json()["result"]["content"]
                else:
                    answer = f"Error {response.status_code}: {response.text}"
            except Exception as e:
                answer = f"❌ Connection error: {e}\n\nThe backend may be starting up — please try again in 30 seconds."

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
