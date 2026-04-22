import streamlit as st
import requests

# --- Configuration ---
# Update this if your FastAPI endpoint name is different (e.g., /ask or /chat)
API_URL = "http://localhost:8000/query" 

st.set_page_config(
    page_title="Forest Carbon Engine",
    page_icon="🌲",
    layout="centered"
)

# --- UI Header ---
st.title("🌲 Forest Carbon Knowledge Engine")
st.markdown("""
Welcome to the AI-powered registry assistant. Ask questions about **Verra** or **ACR** methodologies, 
and the engine will retrieve the exact rules and cite its sources.
""")
st.divider()

# --- Chat History State ---
# This allows the app to remember the conversation while the page is open
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("E.g., What is the baseline scenario for the Sharp Bingham project?"):
    
    # 1. Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Send request to your FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Searching carbon registries..."):
            try:
                # IMPORTANT: Ensure this JSON payload matches your FastAPI Pydantic model
                # If your API expects {"question": prompt}, change "query" to "question" below.
                response = requests.post(API_URL, json={"question": prompt})
                
                if response.status_code == 200:
                    # Adjust 'answer' to match the key returned by your FastAPI dictionary
                    data = response.json()
                    answer = data.get("answer", data.get("response", "Error parsing answer."))
                    
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"API Error {response.status_code}: Make sure your FastAPI backend is running!")
            
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Error: Could not reach the API. Is FastAPI running on localhost:8000?")