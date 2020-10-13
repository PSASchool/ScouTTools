"""Rank teams in upcoming VRC tournament"""

import csv
import json
from urllib.request import urlopen
import pandas as pd
import requests

EVENTCODE = input("Enter the Event Code ")
#SEASON = input('Enter Season - "Change Up" "Tower Takeover" ')
#SEASON = 'Change%20Up'
SEASON = 'Tower%20Takeover'

df = pd.read_html(requests.get(f'https://vexdb.io/events/view/{EVENTCODE}').content)[
    2].to_csv('%s.csv' % EVENTCODE, index=False)
""" Load teams into DataFrame """
df_teams = pd.read_csv('%s.csv' % EVENTCODE)
df_rank = pd.DataFrame()
print(df_teams)

""" Load rankings into file for teams in csv file """
with open('%s.csv' % EVENTCODE, 'r') as f:
    READER = csv.reader(f)
    for team in READER:
        t = team[0]
        with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={t}&season={SEASON}') as resp:
            ratings = resp.read()
            RANK_DATA = json.loads(ratings)
            data = (RANK_DATA['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_rank = df_rank.append(df_temp, ignore_index=True)
print(df_rank)
""" Rename colunms and merge dataframes """
df_rank.columns = ['Team', 'Season', 'Program', 'Vrating_rank', 'Vrating']
df_mrg = pd.merge(df_teams, df_rank, on='Team', how='left', sort=False)

""" print full dataframe to screen """
pd.set_option('display.max_rows', None)
df_mrg.set_index('Team', inplace=True)
print(df_mrg.sort_values(by='Vrating', ascending=False))

""" Export dataframe to excel spreadsheet """
#df_mrg.to_excel(r'%s.xlsx' % EVENTCODE, index=False, header=True)
