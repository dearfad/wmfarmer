import streamlit as st
from scripts.wmmarket import get_items, get_item_info, get_item_orders

st.set_page_config(page_title='Warframe Market Farmer', page_icon='👨‍🌾')

st.write("# Warframe Market Farmer! 👋")

items = get_items()
st.write(f"- 获取列表时间: {items['time']}")
