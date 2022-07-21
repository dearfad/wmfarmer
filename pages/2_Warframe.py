import streamlit as st
from scripts.core import get_warframe_price

warframe_price_df = get_warframe_price()

wcol1 = warframe_price_df.iloc[:10, :]
wcol2 = warframe_price_df.iloc[10:20, :]
wcol3 = warframe_price_df.iloc[20:, :]

col1, col2, col3 = st.columns(3)

with col1:
    st.write(wcol1)
with col2:
    st.write(wcol2)
with col3:
    st.write(wcol3)