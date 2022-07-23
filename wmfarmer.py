import streamlit as st
from scripts.wmmarket import get_items

st.set_page_config(page_title='Warframe Market Farmer', layout="wide", page_icon='👨‍🌾')

st.write("# Warframe Market Farmer! 👨‍🌾")

items = get_items()

if items['time']=='failed':
    st.write(f"➖ ⏱️ **Get Items Failed** ➖ *️⃣ **Status Code: {items[items]}** ➖ 👨‍💼 **By: DEARFAD** ➖")
else:
    st.write(f"➖ ⏱️ **{items['time']}** ➖ *️⃣ **Total: {items['items'].shape[0]}** ➖ 👨‍💼 **By: DEARFAD** ➖")
