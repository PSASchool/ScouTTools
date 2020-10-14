"""Rank teams in upcoming VRC tournament"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv
import json
from urllib.request import urlopen

pd.set_option('display.max_rows', None)

EVENTCODE = 'RE-VRC-20-2420'
#SEASON = input('Enter Season - "Change Up" "Tower Takeover" ')
#SEASON = 'Change%20Up'
#SEASON = 'Tower%20Takeover'

browser = webdriver.Chrome()
browser.get(
    'https://www.robotevents.com/robot-competitions/vex-robotics-competition/RE-VRC-20-2420.html#teams')
time.sleep(10)

df = pd.read_html(browser.page_source)
df[1].to_csv('%s.csv' % EVENTCODE, index=False)
df_teams = pd.read_csv('%s.csv' % EVENTCODE)

""" Load rankings into file for teams in csv file """
# with open('%s.csv' % EVENTCODE, 'r') as f:
#    READER = csv.reader(f)
#    for team in READER:
#        t = team[0]
#        with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={t}&season={SEASON}') as resp:
#            ratings = resp.read()
#            RANK_DATA = json.loads(ratings)
#            data = (RANK_DATA['result'])
#            df_temp = pd.DataFrame.from_dict(data)
#            df_rank = df_rank.append(df_temp, ignore_index=True)
# print(df_rank)
#""" Rename colunms and merge dataframes """
#df_rank.columns = ['Team', 'Season', 'Program', 'Vrating_rank', 'Vrating']
#df_mrg = pd.merge(df_teams, df_rank, on='Team', how='left', sort=False)
#
#""" print full dataframe to screen """
#df_mrg.set_index('Team', inplace=True)
#print(df_mrg.sort_values(by='Vrating', ascending=False))
#
#""" Export dataframe to excel spreadsheet """
##df_mrg.to_excel(r'%s.xlsx' % EVENTCODE, index=False, header=True)
print(df_teams.sort_values(by='Team'))
