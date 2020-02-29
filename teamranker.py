import csv
import json
from urllib.request import urlopen

# Event Code: RE-VRC-19-9740
# EVENCODE = imput("Enter the Event Code")
season = "Tower%20Takover"

with open('teams.csv', 'r') as f:
    reader = csv.reader(f)
    for team in reader:
        t = team[0]
        with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={t}&season=Tower%20Takeover') as resp:
            teams = resp.read()
            RANK_DATA = json.loads(teams)
            print(json.dumps(RANK_DATA, indent=2))
