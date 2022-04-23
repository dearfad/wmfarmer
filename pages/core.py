import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
from pages.wmmarket import get_item_info, get_item_orders

assets_url = "https://warframe.market/static/assets/"


def get_time():
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    time = utc_time.astimezone(
        timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    return time


def markdown_list(itemlist):
    markdown = ""
    if itemlist:
        markdown = '- ' + '\n- '.join(itemlist)
    return markdown


def show_item(url_name):
    item_info = get_item_info(url_name)
    # st.write(item_info)

    item_orders = ''
    if get_item_orders(url_name):
        item_orders = pd.json_normalize(get_item_orders(url_name))
    st.write(item_orders)
    # orders = fmt_item_orders(item_orders)
    # st.write(orders)
    # st.write(orders.columns)
    
    st.write(
        f"**{item_info['zh-hans']['item_name']}** 📝 {item_info['zh-hans']['description']}")
    col0, col1 = st.columns([1, 4])
    col0.write(
        f"[![{item_info['zh-hans']['item_name']}]({assets_url+item_info['thumb']})]({item_info['zh-hans']['wiki_link']})")
    col0.write(
        f"![ducats](https://warframe.market/static/build/resources/images/icons/Ducats.b2f626d13cd31d84117a.png) **{item_info.get('ducats', '--')}**")
    col1.write(f"- {item_info['url_name']}\n{markdown_list(item_info['tags'])}")

    # col1.bar_chart(item_orders[item_orders['order_type']=='buy']['platinum'], height=160, use_container_width=True)
    # col2.write('col2')
    # col1.metric("最高卖出", item_orders['buy'], item_orders['buyer'])
    # col2.metric("最低买入", item_orders['sell'], item_orders['seller'])
    return


if __name__ == '__main__':
    pass
