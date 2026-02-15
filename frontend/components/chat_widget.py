"""
Chat Widget Component
Display chat messages with styling
"""

import streamlit as st


def render_chat_message(message: str, is_user: bool = True):
    """
    Render a chat message bubble
    
    Args:
        message: Message text
        is_user: True if user message, False if agent message
    """
    
    if is_user:
        # User message (right-aligned, blue)
        st.markdown(
            f"""
            <div style="
                background-color: #E3F2FD;
                padding: 12px;
                border-radius: 10px;
                margin: 10px 0;
                margin-left: 20%;
                text-align: left;
            ">
                <strong>You:</strong><br>
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Agent message (left-aligned, green)
        st.markdown(
            f"""
            <div style="
                background-color: #E8F5E9;
                padding: 12px;
                border-radius: 10px;
                margin: 10px 0;
                margin-right: 20%;
                text-align: left;
            ">
                <strong>🤖 Assistant:</strong><br>
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )