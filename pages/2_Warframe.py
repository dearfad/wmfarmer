import streamlit as st
from scripts.core import get_warframe_price

warframe_price_df = get_warframe_price()

wcol1 = warframe_price_df.iloc[:10, :]
wcol2 = warframe_price_df.iloc[10, :]

col1, col2 = st.columns(2)

with col1:
    st.write(wcol1)
with col2:
    st.write(wcol2)