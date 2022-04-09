import streamlit as st
from wmfpkg.droptables import get_droptables
from wmfpkg.wmmarket import get_items
from wmfpkg.wmfcore import show_item


def page():
    items = items()
    droptables = get_droptables()
    st.markdown("最后更新：" + droptables['last_update'])
    item_name = st.text_input('模糊搜索：', 'A1')
    search_result = []
    for key in droptables['relics']:
        if item_name.lower() in key.lower():
            search_result.append(key)
    item_name_cn = []
    for item in search_result:
        item_name_cn.append(
            items[items['item_name_en'] == item]['item_name_cn'].values[0])
    selected_name = st.selectbox('已发现：', item_name_cn)
    selected_relic_name_en = items[items['item_name_cn']
                                   == selected_name]['item_name_en'].values[0]
    relic_drop = droptables['relics'][selected_relic_name_en]
    for item in relic_drop:
        if 'Chassis Blueprint' in item or 'Systems Blueprint' in item or 'Neuroptics Blueprint' in item:
            item = item[:-10]
        item_df = items[items['item_name_en'] == item]
        if item_df.empty:
            if item == 'Forma Blueprint':
                st.markdown('**福马 蓝图**')
                col0, col1, col2 = st.columns(3)
                col0.image(
                    'https://static.wikia.nocookie.net/warframe/images/b/b1/Forma2.png', width=128)
                col1.metric("最高卖出", 0)
                col2.metric("最低买入", 0)
            else:
                st.write(item, '未找到相关信息...')
        else:
            show_item(item_df)
    return
