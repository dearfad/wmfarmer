# Warframe Market Price List - Streamlit
from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import requests
import json
import time
start_time = time.time()
name = 'ash_prime_set'
result = requests.get(f'https://api.warframe.market/v1/items/{name}/orders', headers={'Platform': 'pc'})
st.text(result)
payload = json.loads(result.text)
orders = payload['payload']['orders']
high_buy_price = 0
buy_user = ''
low_sell_price = 0
sell_user = ''
for order in orders:
  if order['order_type']=='sell' and order['user']['status']=='ingame':
    # print('sell', order['platinum'], order['user']['ingame_name'])
    if low_sell_price==0:
      low_sell_price = order['platinum']
      sell_user = order['user']['ingame_name']
    else:
      if order['platinum']<low_sell_price:
        low_sell_price = order['platinum']
        sell_user = order['user']['ingame_name']
  if order['order_type']=='buy' and order['user']['status']=='ingame':
    # print('buy', order['platinum'], order['user']['ingame_name'])
    if high_buy_price==0:
      high_buy_price = order['platinum']
      buy_user = order['user']['ingame_name']
    else:
      if order['platinum']>high_buy_price:
        high_buy_price = order['platinum']
        buy_user = order['user']['ingame_name']
end_time = time.time()
last_time = end_time-start_time
time_text = 'time: '+ str(round(last_time, 3))
st.text(time_text)
st.text(name)
low_price = '低卖：' + str(low_sell_price) + ' ' + sell_user
st.text(low_price)
high_price = '高买：' + str(high_buy_price) + ' ' + buy_user
st.text(high_price)

"""
-DEARFAD-
# Welcome to Streamlit!
Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).
In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
