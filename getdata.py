import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

today = date.today()
DATA_PATH = rf'.\data\{today}'

def read_and_store_data() -> None:
    """
    gets data from leekduck regarding the current raid bosses
    and stores them in a csv file named after today's date
    :return:
    None
    """
    source = requests.get('https://leekduck.com/boss/')
    soup = BeautifulSoup(source.content, features='html.parser')
    raid_list = soup.find('ul', attrs={'class': 'list'})
    raids = raid_list.find_all('li')
    non_boosted_cp = soup.find_all('div', attrs={'class': 'boss-2'})
    pokemon: int = 0
    tier: list = []
    name: list = []
    shiny: list = []
    non_boosted_hundo_cp: list = []
    boosted_hundo_cp: list = []
    boosted_weather: list = []
    current_tier: str = ''
    for raid in raids:
        if raid.find('h2'):
            current_tier = raid.find('h2', attrs={'class': 'boss-tier-header'}).text.strip()
        else:
            tier.append(current_tier)
            name.append(raid.find('p', attrs={'class': 'boss-name'}).text.strip())
            if raid.find('img', attrs={'alt': 'shiny'}):
                is_shiny = True
            else:
                is_shiny = False
            shiny.append(is_shiny)
            non_boosted_hundo_cp.append(non_boosted_cp[pokemon].text.strip().split(' ')[-1])
            boosted_hundo_cp.append(raid.find('span', attrs={'class': 'boosted-cp'}).text.strip().split(' ')[-1])
            boost_weather = [img['title'] for img in raid.find('span', attrs={'class': 'boss-weather'}).find_all('img')]
            e = ''
            for x in boost_weather:
                e += x + ' '
            boosted_weather.append(e)
            pokemon += 1
    data = {
        'tier': tier,
        'name': name,
        'shiny': shiny,
        'non boosted hundo cp': non_boosted_hundo_cp,
        'boosted hundo cp': boosted_hundo_cp,
        'boosted weather': boosted_weather
    }
    pokemon_data = pd.DataFrame(data)
    pokemon_data.to_csv(DATA_PATH, index=False)
