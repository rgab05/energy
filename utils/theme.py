import streamlit as st

def apply_theme(theme_mode):
    body_class = "dark-mode" if theme_mode == "Dark" else "light-mode"
    st.markdown(f'<div class="{body_class}">', unsafe_allow_html=True)
