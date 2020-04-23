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
df1 = pd.read_csv('worlds2020.csv', index_col='Team')

"""Load rankings into file for teams in csv file"""
with open('/home/wandored/PSAorg/TeamRanking/worlds2020.csv', 'r') as f:
    READER = csv.reader(f)
    for team in READER:
        t = team[0]
        with open('rankings.json', 'w') as outfile:
            with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={t}&season={SEASON}') as resp:
                ratings = resp.read()
                RANK_DATA = json.loads(ratings)
                print(json.dumps(RANK_DATA['result'], indent=1))
                json.dump(RANK_DATA['result'], outfile)
