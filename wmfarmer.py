import requests
import pandas as pd

def get_items():
  items_api_url = "https://api.warframe.market/v1/items"
  assets_url = "https://warframe.market/static/assets/"

  r_en = requests.get(items_api_url, headers={"Language": "en"})

  if r_en.status_code == 200:
    items_en = pd.json_normalize(r_en.json()["payload"]["items"])
    items_en.rename(columns={"item_name": "item_name_en"}, inplace=True)

  r_cn = requests.get(items_api_url, headers={"Language": "zh-hans"})

  if r_cn.status_code == 200:
    items_cn = pd.json_normalize(r_cn.json()["payload"]["items"])
    items_cn.rename(columns={"item_name": "item_name_cn"}, inplace=True)

  items = pd.merge(items_cn, items_en)

  # items[items.item_name_cn.duplicated(keep=False)]

  return items

st.write(items)
