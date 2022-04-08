import streamlit as st
from wmfpkg.wmfcore import warframe, nightmare, relic
from wmfpages.item import item

st.set_page_config(page_title='Warframe Market Farmer', page_icon='👨‍🌾')


def main():
    pages = {
        '物品价格': item,
        '战甲套装': warframe,
        '噩梦收益': nightmare,
        '虚空裂缝': relic
    }
    with st.sidebar:
        st.title('Warframe Market Farmer')
        page = st.radio("请选择：", pages.keys())
    pages[page]()


if __name__ == '__main__':
    main()
