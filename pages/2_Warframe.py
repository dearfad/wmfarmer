import streamlit as st
from scripts.core import get_warframe_price

warframe_price_df = get_warframe_price()
st.write(warframe_price_df)