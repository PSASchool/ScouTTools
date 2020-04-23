import requests
import pandas as pd
import csv
import json
from pandas.io.json import json_normalize
from urllib.request import urlopen

SEASON = "Tower%20Takeover"
EVENT = "RE-VRC-19-8379"

df = pd.read_html(requests.get(f'https://www.robotevents.com/robot-competitions/vex-robotics-competition/{EVENT}.html').content)[
    1].to_csv('worlds2020.csv', header=False, index=False)


with open('/home/wandored/PSAorg/TeamRanking/worlds2020.csv', 'r') as f:
    READER = csv.reader(f)
    for team in READER:
        t = team[0]
        with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={t}&season={SEASON}') as resp:
            ratings = resp.read()
            RANK_DATA = json.loads(ratings)
            print(json.dumps(RANK_DATA, indent=2))


# teams = df['Team']

# for i in teams:
#     print(i)
# with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={teams}&SEASON=Tower%20Takover') as resp:
#     worlds = resp.read()
#     RANK_DATA = json.loads(worlds)
#     print(json.dumps(RANK_DATA, indent=2))


# for team in df:
#     t = team[0]
#     print(t)
#
