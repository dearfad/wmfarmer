import streamlit as st
from scripts.wmmarket import items

st.set_page_config(page_title='Warframe Market Farmer', page_icon='👨‍🌾')

st.write("# Warframe Market Farmer! 👋")

st.write(f"- {items()['time']}")
st.write(items()['items'])
