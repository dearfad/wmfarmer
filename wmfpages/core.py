import streamlit as st
from wmfpkg.wmmarket import get_item_info, get_item_orders
import pandas as pd

assets_url = "https://warframe.market/static/assets/"

def fmt_item_orders(item_orders):
    orders = pd.json_normalize(item_orders)
    return orders

def show_item(url_name):
    item_info = get_item_info(url_name)
    # st.write(item_info)
    item_orders = get_item_orders(url_name)
    # orders = fmt_item_orders(item_orders)
    # st.write(item_orders)
    # st.write(orders)
    # st.write(orders.columns)
    st.write(
        f"**{item_info['zh-hans']['item_name']}** 📝 {item_info['zh-hans']['description']}")
    col0, col1, col2 = st.columns(3)
    col0.write(
        f"[![{item_info['zh-hans']['item_name']}]({assets_url+item_info['thumb']})]({item_info['zh-hans']['wiki_link']})")
    col0.write(f"![ducats](https://warframe.market/static/build/resources/images/icons/Ducats.b2f626d13cd31d84117a.png) **{item_info.get('ducats', '--')}**")
    col1.metric("最高卖出", item_orders['buy'], item_orders['buyer'])
    col2.metric("最低买入", item_orders['sell'], item_orders['seller'])
    return


if __name__ == '__main__':
    pass
