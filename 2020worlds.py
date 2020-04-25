"""TeamRanker for 2020 Virtual Worlds"""

import csv
import json
from urllib.request import urlopen
import pandas as pd
import requests

SEASON = "Tower%20Takeover"
EVENT = "RE-VRC-19-8379"

"""Load teams into a csv file"""
df = pd.read_html(requests.get(f'https://www.robotevents.com/robot-competitions/vex-robotics-competition/{EVENT}.html').content)[1].to_csv('worlds2020.csv', index=False)

"""Load teams into DataFrame 1"""
df_teams = pd.read_csv('worlds2020.csv')
df_rank = pd.DataFrame() # initalize dataframe

"""Load rankings into file for teams in csv file"""
with open('worlds2020.csv', 'r') as f:
    READER = csv.reader(f)
    for team in READER:
        t = team[0]
        with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={t}&season={SEASON}') as resp:
            ratings = resp.read()
            RANK_DATA = json.loads(ratings)
            data = (RANK_DATA['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_rank = df_rank.append(df_temp, ignore_index=True)

df_rank.columns = ['Team', 'Season', 'Program', 'Vrating_rank', 'Vrating'] #rename colunms
df_mrg = pd.merge(df_teams, df_rank, on='Team', how='left', sort=False) # merge dataframes
#pd.set_option('display.max_rows', None)
#print(df_mrg)
df_mrg.to_excel(r'worlds2020.xlsx', index=False, header=True) # export dataframe to excel spreadsheet
