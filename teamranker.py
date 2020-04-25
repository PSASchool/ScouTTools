"""Rank teams in upcoming VRC tournament"""

import csv
import json
from urllib.request import urlopen
import pandas as pd
import requests

EVENTCODE = input("Enter the Event Code ")
#SEASON = input('Enter Season - "Change Up" "Tower Takeover" ')
SEASON = 'Tower%20Takeover'

df = pd.read_html(requests.get(f'https://www.robotevents.com/robot-competitions/vex-robotics-competition/{EVENTCODE}.html').content)[2].to_csv('%s.csv' % EVENTCODE, index=False)

""" Load teams into DataFrame """
df_teams = pd.read_csv('%s.csv' % EVENTCODE)
df_rank = pd.DataFrame()

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

df_rank.columns = ['Team', 'Season', 'Program', 'Vrating_rank', 'Vrating'] #rename colunms
df_mrg = pd.merge(df_teams, df_rank, on='Team', how='left', sort=False) # merge dataframes
#pd.set_option('display.max_rows', None) # this and next line used for dbuggin
#print(df_mrg)
df_mrg.to_excel(r'%s.xlsx' % EVENTCODE, index=False, header=True) # export dataframe to excel spreadsheet
