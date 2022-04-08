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


def item():
    item_name = st.text_input('模糊搜索：', 'Xiphos 机身')
    items = get_items()
    search_result = items[items['item_name_cn'].str.contains(
        item_name, case=False)]
    item_names = search_result['item_name_cn'].values
    selected_name = st.selectbox('已发现：', item_names)
    item_df = items[items['item_name_cn'] == selected_name]
    if item_df.empty:
        st.warning('未找到相关信息...')
    else:
        show_item(item_df)
    return


def nightmare():
    nightmaremoderewards = ['Ice Storm', 'Stunning Speed', 'Hammer Shot', 'Wildfire', 'Accelerated Blast', 'Blaze', 'Chilling Reload', 'Drifting Contact', 'Seeking Fury',
                            'Armored Agility', 'Shred', 'Rending Strike', 'Fortitude', 'Streamlined Form', 'Animal Instinct', 'Vigor', 'Lethal Torrent', 'Focus Energy', 'Constitution']
    items = get_items()
    for item_name in nightmaremoderewards:
        item_df = items[items['item_name_en'] == item_name]
        show_item(item_df)
        # r_a = '水星 金星 地球 火星'
        # r_b = '火卫一 谷神星 木星 欧罗巴 土星 月球 虚空 赤毒要塞 火卫二'
        # r_c = '天王星 海王星 冥王星 阋神星 赛德娜'
        # night['位置'] = [r_a,r_a,r_a,r_a,r_a,r_a,r_a,r_b,r_b,r_b,r_b,r_b,r_b,r_c,r_c,r_c,r_c,r_c,r_c,]
        # st.table(night)
    return


def warframe():
    warframe_prime_list = ['ash', 'atlas', 'banshee', 'chroma', 'ember', 'equinox', 'frost', 'gara', 'garuda', 'harrow', 'hydroid', 'inaros', 'ivara', 'limbo', 'loki', 'mag',
                           'mesa', 'mirage', 'nekros', 'nezha', 'nidus', 'nova', 'nyx', 'oberon', 'octavia', 'rhino', 'saryn', 'titania', 'trinity', 'valkyr', 'vauban', 'volt', 'wukong', 'zephyr']
    warframe_prime_set_list = ['set', 'blueprint',
                               'neuroptics', 'chassis', 'systems']
    warframe_selection = st.selectbox('选择战甲', warframe_prime_list)
    items = get_items()
    for item in warframe_prime_set_list:
        item_name = warframe_selection + '_prime_' + item
        item_df = items[items['url_name'] == item_name]
        show_item(item_df)
    return


def relic():
    items = get_items()
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

if __name__ == '__main__':
    # pages = {
    #     '物品价格': item,
    #     '战甲套装': warframe,
    #     '噩梦收益': nightmare,
    #     '虚空裂缝': relic
    # }
    pass