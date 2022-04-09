import streamlit as st
from wmfpkg.wmmarket import get_item_info, items_orders

assets_url = "https://warframe.market/static/assets/"


def show_item(url_name):
    item = get_item_info(url_name)
    order_info = items_orders(url_name)
    st.write(order_info)
    st.write(f"**{item['zh-hans']['item_name']}** [🔗]({item['zh-hans']['wiki_link']} 'wiki') {item['zh-hans']['description']}")
    col0, col1, col2 = st.columns(3)
    col0.image(assets_url+item['icon'])
    col0.write(item['zh-hans']['drop'])
    col1.metric("最高卖出", order_info['buy'], order_info['buyer'])
    col2.metric("最低买入", order_info['sell'], order_info['seller'])
    return


if __name__ == '__main__':
    # pages = {
    #     '物品价格': item,
    #     '战甲套装': warframe,
    #     '噩梦收益': nightmare,
    #     '虚空裂缝': relic
    # }
    pass
