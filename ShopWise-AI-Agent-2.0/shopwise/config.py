import os
import streamlit as st
def get_secret(name):
    try:
        value=st.secrets.get(name)
        if value: return value
    except Exception: pass
    return os.getenv(name)
