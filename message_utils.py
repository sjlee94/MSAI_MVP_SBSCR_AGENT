import streamlit as st

def init_messages():
    if "messages" not in st.session_state:
        # initialize prompt with system message
        st.session_state.messages = [
            {
                "role": "system",
                "content": """You are an agent that summarizes and explains subscriber performance data, 
                            or provides detailed explanations about pricing plans."""
            },
        ]