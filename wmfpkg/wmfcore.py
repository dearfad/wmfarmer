import streamlit as st
from wmfpkg.droptables import get_droptables
from wmfpkg.wmmarket import get_items, get_order_info

assets_url = "https://warframe.market/static/assets/"


def show_item(item_df):
    item = item_df.to_dict(orient='records')[0]
    thumb_url = assets_url + item['thumb']
    order_info = get_order_info(item['url_name'])
    st.markdown('**'+item['item_name_cn']+'**'+'  '+order_info['time'])
    col0, col1, col2 = st.columns(3)
    col0.image(thumb_url)
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
