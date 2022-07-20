import streamlit as st
import requests
from bs4 import BeautifulSoup

droptables_url = 'https://www.warframe.com/droptables'

@st.cache(show_spinner=False, suppress_st_warning=True)
def get_droptables():
    droptables = {}
    r = requests.get(droptables_url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, features='html.parser')
        last_update = soup.p.contents[1].strip()
        droptables['last_update'] = last_update
        toc = soup.ul
        dynamic_location_rewards = soup.ul.ul
        toc_dict = {}
        for item in toc:
            if item.name:
                toc_dict[item.a.text] = item.a['href'].strip('#')
        dynamic_location_rewards_dict = {}
        for item in dynamic_location_rewards:
            if item.name:
                dynamic_location_rewards_dict[item.a.text] = item.a['href'].strip('#')
        # Relics
        id = toc_dict['Relics']
        relic_dict = {}
        relics = soup.find('h3', id=id)
        relics_table = relics.next_sibling.next_sibling
        relic_count = int(len(relics_table.find_all('tr'))/8/4)
        relic_tag = relics_table.tr
        for i in range(relic_count+1):
            relic_drops = {}
            relic_name = relic_tag.text.split(' (')[0]
            for n in range(6):
                relic_tag = relic_tag.next_sibling
                relic_drops[relic_tag.td.text] = int(
                    relic_tag.td.next_sibling.text.split('.')[0].split('(')[1])
            relic_drops = sorted(relic_drops.items(),
                                 key=lambda x: x[1], reverse=True)
            relic_dict[relic_name] = [x[0] for x in relic_drops]
            for n in range(34):
                if relic_tag.next_sibling:
                    relic_tag = relic_tag.next_sibling
        droptables['relics'] = relic_dict
        # Nightmare
        nightmare_dict = {}
        droptables['nightmare'] = nightmare_dict
    return droptables


if __name__ == '__main__':
    droptables = get_droptables()
    print(droptables.keys())
