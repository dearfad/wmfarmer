import streamlit as st
from wmfpkg.wmmarket import get_item_info, get_item_orders

assets_url = "https://warframe.market/static/assets/"


def show_item(url_name):
    item_info = get_item_info(url_name)
    item_orders = get_item_orders(url_name)
    st.write(
        f"**{item_info['zh-hans']['item_name']}** 📝 {item_info['zh-hans']['description']}")
    col0, col1, col2 = st.columns(3)
    col0.write(
        f"[![{item_info['zh-hans']['item_name']}]({assets_url+item_info['thumb']})]({item_info['zh-hans']['wiki_link']})")
    col1.metric("最高卖出", item_orders['buy'], item_orders['buyer'])
    col2.metric("最低买入", item_orders['sell'], item_orders['seller'])
    return


if __name__ == '__main__':
    pass
