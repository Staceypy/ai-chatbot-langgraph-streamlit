import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    [data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, #E8F0FE 0%, #FFE1E7 100%);
    }
    [data-testid="stSidebar"] > div:first-child {
        background-image: linear-gradient(180deg, #E8F0FE 0%, #FFE1E7 100%);
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    .stButton>button {
        border-radius: 20px;
        padding: 0.5rem 2rem;
        background-image: linear-gradient(120deg, #89CFF0 0%, #FFB6C1 100%);
        border: none;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        color: #1E4C56;
    }
    button[data-testid="StyledFullScreenButton"] {
        background-image: linear-gradient(120deg, #89CFF0 0%, #FFB6C1 100%);
        color: white;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .user-message {
        background-color: #E8F0FE;
    }
    .ai-message {
        background-color: #F0F2F6;
    }
    .stTextArea textarea:focus {
        border-color: #46B1C9 !important;
        box-shadow: 0 0 0 0.2rem rgba(137, 207, 240, 0.25) !important;
    }
    
    
    [data-baseweb="textarea"]:focus-within {
        border-color: #89CFF0 !important;
        box-shadow: 0 0 0 0.2rem rgba(137, 207, 240, 0.25) !important;
        outline: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/chat"
MODEL_NAMES = ["llama3-70b-8192", "mixtral-8x7b-32768"]

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    selected_model = st.selectbox("Select Model:", MODEL_NAMES)
    given_system_prompt = st.text_area(
        "Define your AI Assistant:",
        height=150,
        placeholder="I am an AI assistant that helps with..."
    )
    st.markdown("---")
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

# Main chat interface
st.title("🤖 AI Assistant")
st.markdown("---")

# Chat history display
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <span>👤</span>
                <div>{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message ai-message">
                <span>🤖</span>
                <div>{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

# User input
with st.container():
    user_input = st.text_area("Your message:", height=100, placeholder="Type your message here...")
    col1, col2 = st.columns([6, 1])
    with col2:
        send_button = st.button("Send 📤", use_container_width=True)

if send_button and user_input.strip():
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
    
    try:
        with st.spinner("AI is thinking..."):
            payload = {
                "messages": [user_input],
                "model_name": selected_model,
                "system_prompt": given_system_prompt
            }
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    ai_responses = [
                        message.get("content", "")
                        for message in response_data.get("messages", [])
                        if message.get("type") == "ai"
                    ]
                    
                    if ai_responses:
                        ai_response = ai_responses[-1]
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": ai_response,
                            "timestamp": datetime.now()
                        })
                        st.rerun()
                    else:
                        st.warning("No response generated.")
            else:
                st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        
# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
