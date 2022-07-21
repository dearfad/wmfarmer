import streamlit as st
from scripts.core import get_warframe_price

warframe_price_df = get_warframe_price()

wcol1 = warframe_price_df.iloc[:10, :]
wcol2 = warframe_price_df.iloc[10:20, :]
wcol3 = warframe_price_df.iloc[20:30, :]
wcol4 = warframe_price_df.iloc[30:, :]

col1, col2 = st.columns(2)

with col1:
    st.table(wcol1)
with col2:
    st.table(wcol2)

col3, col4 = st.columns(2)
with col3:
    st.write(wcol3)
with col4:
    st.write(wcol4)