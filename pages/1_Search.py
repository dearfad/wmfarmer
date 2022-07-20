import streamlit as st
from scripts.wmmarket import items, item_info, item_orders
from scripts.core import item_price

assets_url = "https://warframe.market/static/assets/"

items = items()['items']

input_name = st.text_input('模糊搜索：', '')
search_result = items[items['item_name'].str.contains(input_name.strip(), case=False)]
if search_result.empty:
    st.warning('未找到相关信息...')
else:
    selected_name = st.selectbox('已发现：', search_result['item_name'])
    url_name = search_result[search_result['item_name']==selected_name]['url_name'].values[0]
    item_info = item_info(url_name)
    item_orders = item_orders(url_name)
    st.write(f"➖ ⏱️ **Info: {item_info['time'].split()[1]}** ➖ ⏲️ **Orders: {item_orders['time'].split()[1]}** ➖")
    st.write(f"### **{item_info['info']['zh-hans']['item_name']}**")

    price_col, thumb_col, description_col = st.columns([1,2,4])
    with price_col:        
        item_price = item_price(item_orders['orders'])
        st.metric(label='最低卖价', value=item_price['ingame_lowest_sell_platinum'])
        st.metric(label='最高买价', value=item_price['ingame_highest_buy_platinum'])
    with thumb_col:
        wiki_link = item_info['info']['zh-hans']['wiki_link']
        if wiki_link:
            st.write(f"[![{item_info['info']['zh-hans']['item_name']}]({assets_url+item_info['info']['thumb']})]({item_info['info']['zh-hans']['wiki_link']})")
        else:
            st.write(f"[![{item_info['info']['zh-hans']['item_name']}]({assets_url+item_info['info']['thumb']})]")
    with description_col:
        st.write(f"![ducats](https://warframe.market/static/build/resources/images/icons/Ducats.b2f626d13cd31d84117a.png) **{item_info['info'].get('ducats', '--')}**")
        st.write(f"📝 {item_info['info']['zh-hans']['description']}")
    