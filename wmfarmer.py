import streamlit as st
from scripts.wmmarket import get_items

st.set_page_config(page_title='Warframe Market Farmer', layout="wide", page_icon='👨‍🌾')

st.write("# Warframe Market Farmer! 👨‍🌾")

if get_items()['time']=='failed':
    st.write(f"➖ ⏱️ **Get Items Failed** ➖ *️⃣ **Status Code: {get_items()[items]}** ➖ 👨‍💼 **By: DEARFAD** ➖")
else:
    st.write(f"➖ ⏱️ **{get_items()['time']}** ➖ *️⃣ **Total: {get_items()['items'].shape[0]}** ➖ 👨‍💼 **By: DEARFAD** ➖")
