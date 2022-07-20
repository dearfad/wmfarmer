import streamlit as st
import pandas as pd

from scripts.wmmarket import item_info, item_orders

assets_url = "https://warframe.market/static/assets/"


def show_item_info(item_info):
    st.write(
        f"[![{item_info['zh-hans']['item_name']}]({assets_url+item_info['thumb']})]({item_info['zh-hans']['wiki_link']})")
    st.write(
        f"![ducats](https://warframe.market/static/build/resources/images/icons/Ducats.b2f626d13cd31d84117a.png) **{item_info.get('ducats', '--')}**")
    return


def fmt_item_orders(orders_df):
    # orders_dict = {
    #     'ingame_highest_buy_platinum': 0,
    #     'ingame_highest_buyer': '',
    #     'ingame_high_buy': pd.DataFrame(),
    #     'week_high_buy_platinum': 0,
    #     'ingame_lowest_sell_platinum': 0,
    #     'ingame_lowest_seller': '',
    #     'ingame_low_sell': pd.DataFrame(),
    #     'week_low_sell_platinum': 0,        
    # }
    # # st.write(orders_df)

    # # ingame_hightest_buy
    # ingame_buy_orders = orders_df[(orders_df['user.status'] == 'ingame') & (
    #     orders_df['order_type'] == 'buy')].sort_values(by='platinum', ascending=False)
    # if not ingame_buy_orders.empty:
    #     orders_dict['ingame_highest_buy_platinum'] = ingame_buy_orders.iloc[0].at['platinum']
    #     orders_dict['ingame_highest_buyer'] = ingame_buy_orders.iloc[0].at['user.ingame_name']
    #     orders_dict['ingame_high_buy'] = ingame_buy_orders.head(5)
    # # week_high_buy

    # # ingame_lowest_sell
    # ingame_sell_orders = orders_df[(orders_df['user.status'] == 'ingame') & (
    #     orders_df['order_type'] == 'sell')].sort_values(by='platinum', ascending=True)
    # if not ingame_sell_orders.empty:
    #     orders_dict['ingame_lowest_sell_platinum'] = ingame_sell_orders.iloc[0].at['platinum']
    #     orders_dict['ingame_lowest_seller'] = ingame_sell_orders.iloc[0].at['user.ingame_name']
    #     orders_dict['ingame_low_sell'] = ingame_sell_orders.head(5)
    # # week_low_sell

    return orders_dict


def show_item_orders(orders):
    # if orders:
    #     orders_df = pd.json_normalize(orders)
    #     orders_dict = fmt_item_orders(orders_df)
    #     st.write(f"当前最高买价：{orders_dict['ingame_highest_buy_platinum']}")
    #     st.write(f"当前最高买者：{orders_dict['ingame_highest_buyer']}")
    #     st.write("七日内最高买价：")
    #     with st.expander('买单列表'):
    #         if not orders_dict['ingame_high_buy'].empty:
    #             st.write(orders_dict['ingame_high_buy'][['platinum','last_update','user.ingame_name']])
    #     st.write(f"当前最低卖价：{orders_dict['ingame_lowest_sell_platinum']}")
    #     st.write(f"当前最低卖者：{orders_dict['ingame_lowest_seller']}")
    #     st.write("七日内最高卖价：")
    #     with st.expander('卖单列表'):
    #         if not orders_dict['ingame_low_sell'].empty:
    #             st.write(orders_dict['ingame_low_sell'][['platinum','last_update','user.ingame_name']])
    return


def show_item(url_name, info, orders):

    st.write(f"### **{info['zh-hans']['item_name']}**")
    # st.write(f"📝 {info['zh-hans']['description']}")

    # show_item_info(info)

    # show_item_orders(orders)

    return

