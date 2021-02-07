import pandas as pd
import re
import csv
import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import config  # This file contains the bearer key

headers = {
    'Authorization': 'Bearer ' + config.api_userkey,
    'Content-Type': 'application/json; charset=utf-8'
}

query = {

}


def make_dataframe(file):
    with open(file) as resp:
        dframe = pd.DataFrame()
        db = resp.read()
        db_data = json.loads(db)
        data = (db_data['data'])
        df_temp = pd.DataFrame.from_dict(data)
        dframe = dframe.append(df_temp, ignore_index=True)
        return(dframe)


def get_codes():
    # EVENT_REGION = input('Enter the Event Region you wish to search ')
    EVENT_REGION = 'South Carolina'
    # GRADE_LEVEL = input('Enter grade level - "middle school" or "high school" ')
    GRADE_LEVEL = 'High School'
    # SEASON = input('Enter the current Season ')
    # SEASON = 'Change Up'

    # Scrape events from robotevents.com based on inputs
    browser = webdriver.Chrome()
    browser.get('https://www.robotevents.com/robot-competitions/vex-robotics-competition?seasonId=&eventType=&name=&grade_level_id=&level_class_id=&from_date=10%2F06%2F2020&to_date=&event_region=2490&country_id=*&city=&affiliation_id=')
    grade = browser.find_element_by_name('grade_level_id')
    grade.send_keys(f'{GRADE_LEVEL}')
    grade.send_keys(Keys.TAB)
    region = browser.find_element_by_name('event_region')
    region.send_keys(f'{EVENT_REGION}')
    region.send_keys(Keys.TAB)

    # Find event links and pluck out the event codes
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.close()
    links = soup.find_all('a')

    comps = []
    for link in links:
        if 'VRC' in link.text:
            comps.append(link.attrs['href'])

    events = []
    for comp in comps:
        if 'RE-VRC-' in comp:
            events.append(re.findall(
                r'RE-VRC-[0-9][0-9]-[0-9][0-9][0-9][0-9]', comp))

    # Creates a list of clean event codes
    skus = [''.join(eve) for eve in events]
    return skus


df_competitions = pd.DataFrame()

sku_list = get_codes()

for sku in sku_list:
    resp = requests.get(
        f'https://www.robotevents.com/api/v2/events?sku%5B%5D={sku}')
    print(resp)
    resp_dict = resp.json()
    df_temp = pd.DataFrame.from_dict(resp_dict)
    df_competitions = df_competitions.append(df_temp, ignore_index=True)

print(df_competitions)
# df_event = make_dataframe('./data/events.json')
# df_event.drop(columns=(['start', 'end', 'season', 'program', 'location',
#                        'divisions', 'level', 'ongoing', 'event_type']), inplace=True)
# df_seasons = make_dataframe('./data/seasons.json')
# df_seasons[['A', 'Name']
#           ] = df_seasons['name'].str.split(pat=':', expand=True)
# df_seasons.drop(
#    columns=(['name', 'program', 'start', 'end', 'A']), inplace=True)
# df_teams = make_dataframe('./data/event_teams.json')
# df_teams.drop(columns=(['location', 'registered', 'program']), inplace=True)
# print(df_event)
# print(df_seasons)
# print(df_teams)

# for d in data['data']:
#    name = d['name']
#    print(name)


# for code in sku_list:
#    browser = webdriver.Chrome()
#    browser.get(
#        f'https://www.robotevents.com/robot-competitions/vex-robotics-competition/{code}.html')
#    soup = BeautifulSoup(browser.page_source, 'lxml')
#    browser.close()
#    events = soup.find('h3')
#    event_list.append(events.get_text().strip())
#
# s_event = pd.Series(event_list)
# df_competitions = pd.concat([s_sku, s_event], axis=1)
#
# df_competitions[['A', 'B']
#                ] = df_competitions[1].str.split(pat='(', expand=True)
# df_competitions[['X', 'EventName']] = df_competitions['A'].str.split(
#    pat='VRC', expand=True)
# df_competitions[['GradeLevel', 'Type', 'Judging']
#                ] = df_competitions['B'].str.split(pat=',', expand=True)
# df_competitions.drop(columns=([1, 'A',  'X', 'B']), inplace=True)
# df_competitions.rename(columns={0: 'EventCode'}, inplace=True)
# df_competitions = df_competitions.drop(
#    df_competitions[df_competitions.GradeLevel == 'MS Only'].index)
# df_competitions.to_csv('./output/competitions.csv', index=False)

# This part will pull all the teams and write them to excel.  (move this to teamranker)
# with pd.ExcelWriter(f'./output/{SEASON}.xlsx') as writer:  # pylint: disable=abstract-class-instantiated
#    for event in event_list:
#        browser = webdriver.Chrome()
#        browser.get(
#            f'https://www.robotevents.com/robot-competitions/vex-robotics-competition/{event}.html#teams')
#        time.sleep(5)
#        df = pd.read_html(browser.page_source)
#        browser.close()
#        df[0].to_csv('./output/%s.csv' % event, index=False)
#        df_event = pd.read_csv('./output/%s.csv' % event)
#        try:
#            print(event)
#            print(df_event.sort_values(by='Team', ascending=False))
#            df_event.to_excel(writer, sheet_name=event, index=False)
#            print()
#        except:
#            df[1].to_csv('./output/%s.csv' % event, index=False)
#            df_event = pd.read_csv('./output/%s.csv' % event)
#            print(event)
#            print(df_event.sort_values(by='Team', ascending=False))
#            df_event.to_excel(writer, sheet_name=event, index=False)
#            print()
