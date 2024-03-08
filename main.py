import streamlit as st
import pandas as pd
from datetime import date
from getdata import read_and_store_data
import os

today: date = date.today()
df: pd.DataFrame
if os.path.exists(f'{today}.csv'):
    df = pd.read_csv(f'{today}.csv')
else:
    read_and_store_data()
    df = pd.read_csv(f'{today}.csv')

tiers = st.multiselect(
    'Choose Tiers',
    ['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Tier 5', 'Tier 6', 'Mega', 'Elite'],
    ['Tier 5'])
my_button = st.button('get info')
if my_button:
    if not tiers:
        st.error('Please select at least one tier.')
    else:
        pokemon_data = df[df['tier'].isin(tiers)]
        to_copy: str = ''
        for index, row in pokemon_data.iterrows():
            shiny_emoji = '✨' if row['shiny'] else ''
            to_copy += (f'{row['tier']} {row['name']} {shiny_emoji}'
                        f'\n{row['non boosted hundo cp']} / {row['boosted hundo cp']}'
                        f'\n{row['boosted weather']}\n')
        st.code(to_copy, language="python")
        st.write(pokemon_data)
