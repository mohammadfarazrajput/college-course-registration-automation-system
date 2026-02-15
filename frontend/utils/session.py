"""
Session State Management
Handles login state and student data
"""

import streamlit as st


def init_session():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'student' not in st.session_state:
        st.session_state.student = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'selected_courses' not in st.session_state:
        st.session_state.selected_courses = []


def get_student():
    """Get current student data"""
    return st.session_state.get('student')


def set_student(student_data):
    """Set student data and mark as logged in"""
    st.session_state.student = student_data
    st.session_state.logged_in = True


def clear_session():
    """Clear all session data (logout)"""
    st.session_state.logged_in = False
    st.session_state.student = None
    st.session_state.chat_history = []
    st.session_state.selected_courses = []


def is_logged_in():
    """Check if user is logged in"""
    return st.session_state.get('logged_in', False)
