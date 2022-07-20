import streamlit as st
from scripts.wmmarket import items

st.set_page_config(page_title='Warframe Market Farmer', page_icon='👨‍🌾')

st.write("# Warframe Market Farmer! 👨‍🌾")

if items()['time']=='failed':
    st.write(f"- **Failed!**")
    st.write(f"- **Status Code**: **{items()[items]}**")
else:
    st.write(f"➖ ⏱️ **{items()['time']}** ➖ *️⃣ **Total: {items()['items'].shape[0]}** ➖")
