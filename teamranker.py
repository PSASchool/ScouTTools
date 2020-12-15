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

df_competitions = pd.read_csv('./output/competitions.csv')
print(df_competitions)

EVENTCODE = input('Enter the Event Code you want to rank ')

browser = webdriver.Chrome()
browser.get(
    f'https://www.robotevents.com/robot-competitions/vex-robotics-competition/{EVENTCODE}.html#teams')

df = pd.read_html(browser.page_source)
browser.close()
print(df)
try:
    df[0].to_csv('./output/%s.csv' % EVENTCODE, index=False)
    df_teams = pd.read_csv('./output/%s.csv' % EVENTCODE)
    team_list = df_teams['Team']
except:
    df[1].to_csv('./output/%s.csv' % EVENTCODE, index=False)
    df_teams = pd.read_csv('./output/%s.csv' % EVENTCODE)
    team_list = df_teams['Team']

print(team_list)
# This part will pull all the teams and write them to excel.  (move this to teamranker)
# with pd.ExcelWriter(f'./output/{EVENTCODE}.xlsx') as writer:  # pylint: disable=abstract-class-instantiated


# with open('./output/%s.csv' % EVENTCODE, 'r') as f:
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
##df_mrg.to_excel(f'./output/%s.xlsx' % EVENTCODE, index=False, header=True)
print(df_teams.sort_values(by='Team'))
