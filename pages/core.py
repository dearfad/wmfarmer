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


def fmt_item_orders(orders_df):
    orders_dict = {
        'ingame_highest_buy_platinum': 0,
        'ingame_hightest_buyer': '',
        'ingame_lowest_sell_platinum': 0,
        'ingame_lowest_seller': '',
    }

    # ingame_hightest_buy
    ingame_buy_orders = orders_df[(orders_df['user.status'] == 'ingame') & (
        orders_df['order_type'] == 'buy')].sort_values(by='platinum', ascending=False)
    # st.write(ingame_buy_orders)
    orders_dict['ingame_highest_buy_platinum'] = ingame_buy_orders.iloc[0].at['platinum']
    orders_dict['ingame_hightest_buyer'] = ingame_buy_orders.iloc[0].at['user.ingame_name']

    # ingame_lowest_sell
    ingame_sell_orders = orders_df[(orders_df['user.status'] == 'ingame') & (
        orders_df['order_type'] == 'sell')].sort_values(by='platinum', ascending=True)
    st.write(ingame_sell_orders)
    orders_dict['ingame_highest_sell_platinum'] = ingame_sell_orders.iloc[0].at['platinum']
    orders_dict['ingame_hightest_seller'] = ingame_sell_orders.iloc[0].at['user.ingame_name']


    return orders_dict


def show_item_orders(orders):
    if orders:
        orders_df = pd.json_normalize(orders)
        orders_dict = fmt_item_orders(orders_df)
        st.write(orders_dict)
    return


def show_item(url_name, info, orders):

    st.write(
        f"**{info['zh-hans']['item_name']}** 📝 {info['zh-hans']['description']}")

    col0, col1 = st.columns([1, 4])

    with col0:
        show_item_info(info)

    with col1:
        show_item_orders(orders)

    return


if __name__ == '__main__':
    pass
