import streamlit as st
import pandas as pd
from datetime import date
from getdata import read_and_store_data
import os
from PIL import Image

today: date = date.today()
df: pd.DataFrame
DATA_DIR = r'data'
DATA_PATH = rf'data/{today}'
FAVICO = r'arceus-logo.png'

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    read_and_store_data()
    df = pd.read_csv(DATA_PATH)

favico = Image.open(FAVICO)
st.set_page_config(
    page_title='PoGo raid bosses',
    page_icon=favico
)

st.title('PokemonGo current Raid bosses')
st.divider()

tiers = st.multiselect(
    'Choose Tiers',
    ['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Tier 5', 'Tier 6', 'Mega', 'Elite'],
    ['Tier 5'])
my_button = st.button('Get info')
if my_button:
    if not tiers:
        st.error('Please select at least one tier.')
    else:
        pokemon_data = df[df['tier'].isin(tiers)]
        to_copy: str = ''
        for index, row in pokemon_data.iterrows():
            shiny_emoji = '✨' if row['shiny'] else ''
            to_copy += f"{row['tier']} | {row['name']} {shiny_emoji} \n{row['non boosted hundo cp']} / {row['boosted hundo cp']} \n{row['boosted weather']}\n\n"
        header = '👾 current raid bosses👾\n\n'
        st.code(header + to_copy, language='text')

st.divider()
st.subheader('About this project')
st.write('''
This website allows you to have information about current raid bosses in Pokemon Go.
Making this possible is a huge thanks to https://leekduck.com/boss/ for the data has to be scrapped from the website.
This solves a problem that out local community faces that is to have a message that includes information about raid
bosses and share it with community with extra features like having a hundo cp and a boosted hundo cp mentioned.
''')
