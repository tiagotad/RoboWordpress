import os

def _get_secret(key, default=None):
    try:
        import streamlit as st
        return st.secrets.get(key, default)
    except Exception:
        return default

WP_URL = _get_secret('WP_URL')
WP_USER = _get_secret('WP_USER')
WP_PASSWORD = _get_secret('WP_PASSWORD')
OPENAI_API_KEY = _get_secret('OPENAI_API_KEY')
GOOGLE_SHEET_NAME = _get_secret('GOOGLE_SHEET_NAME', _get_secret('GOOGLE_SHEET'))
GOOGLE_SHEET_ID = _get_secret('GOOGLE_SHEET_ID')
