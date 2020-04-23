#! /usr/bin/env python
import csv
import json
from urllib.request import urlopen

# EVENTCODE = input("Enter the Event Code")
EVENTCODE = "RE-VRC-19-8379"
SEASON = "Tower%20Takeover"

with open('/home/wandored/PSAorg/TeamRanking/teams.csv', 'r') as f:
    READER = csv.reader(f)
    for team in READER:
        t = team[0]
        with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={t}&season={SEASON}') as resp:
            teams = resp.read()
            RANK_DATA = json.loads(teams)
            print(json.dumps(RANK_DATA, indent=2))
