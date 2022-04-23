import streamlit as st
import pandas as pd

from pages.wmmarket import get_item_info, get_item_orders

assets_url = "https://warframe.market/static/assets/"


def show_item_info(item_info):
    st.write(
        f"[![{item_info['zh-hans']['item_name']}]({assets_url+item_info['thumb']})]({item_info['zh-hans']['wiki_link']})")
    st.write(
        f"![ducats](https://warframe.market/static/build/resources/images/icons/Ducats.b2f626d13cd31d84117a.png) **{item_info.get('ducats', '--')}**")
    return


def fmt_item_orders(item_orders):
    return item_orders


def show_item_orders(item_orders):
    st.write(item_orders)


def show_item(url_name, info, orders):

    st.write(url_name)
    st.write(info)
    st.write(orders)

    # st.write(
    #     f"**{item_info['zh-hans']['item_name']}** 📝 {item_info['zh-hans']['description']}")

    # item_orders = ''
    # if get_item_orders(url_name):
    #     item_orders = pd.json_normalize(get_item_orders(url_name))


    # col0, col1 = st.columns([1, 4])

    # with col0:
    #     show_item_info(item_info)

    # with col1:
    #     show_item_orders(item_orders)

    # col1.bar_chart(item_orders[item_orders['order_type']=='buy']['platinum'], height=160, use_container_width=True)
    # col2.write('col2')
    # col1.metric("最高卖出", item_orders['buy'], item_orders['buyer'])
    # col2.metric("最低买入", item_orders['sell'], item_orders['seller'])
    return


if __name__ == '__main__':
    pass
