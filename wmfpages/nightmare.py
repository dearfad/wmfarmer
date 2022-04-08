import streamlit as st
from wmfpkg.wmmarket import get_items
from wmfpkg.wmfcore import show_item


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
