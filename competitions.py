from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import csv


# EVENT_REGION = input('Enter the Event Region you wish to search ')
EVENT_REGION = 'South Carolina'
# GRADE_LEVEL = input('Enter grade level - "middle school" or "high school" ')
GRADE_LEVEL = 'High School'
# SEASON = input('Enter the current Season ')
SEASON = 'Change Up'

browser = webdriver.Chrome()
browser.get('https://www.robotevents.com/robot-competitions/vex-robotics-competition?seasonId=&eventType=&name=&grade_level_id=&level_class_id=&from_date=10%2F06%2F2020&to_date=&event_region=2490&country_id=*&city=&affiliation_id=')

grade = browser.find_element_by_name('grade_level_id')
grade.send_keys(f'{GRADE_LEVEL}')
grade.send_keys(Keys.RETURN)
region = browser.find_element_by_name('event_region')
region.send_keys(f'{EVENT_REGION}')
region.send_keys(Keys.TAB)

time.sleep(5)

comps = []
events = []
soup = BeautifulSoup(browser.page_source, 'lxml')
browser.close()
links = soup.find_all('a')
for link in links:
    if 'VRC' in link.text:
        comps.append(link.attrs['href'])

for comp in comps:
    if 'RE-VRC-' in comp:
        events.append(re.findall(
            r'RE-VRC-[0-9][0-9]-[0-9][0-9][0-9][0-9]', comp))
event_list = [''.join(ele) for ele in events]

with pd.ExcelWriter(f'{SEASON}.xlsx') as writer:  # pylint: disable=abstract-class-instantiated
    for event in event_list:
        browser = webdriver.Chrome()
        browser.get(
            f'https://www.robotevents.com/robot-competitions/vex-robotics-competition/{event}.html#teams')
        time.sleep(5)
        df = pd.read_html(browser.page_source)
        browser.close()
        df[0].to_csv('%s.csv' % event, index=False)
        df_event = pd.read_csv('%s.csv' % event)
        try:
            print(event)
            print(df_event.sort_values(by='Team', ascending=False))
            df_event.to_excel(writer, sheet_name=event, index=False)
            print()
        except:
            df[1].to_csv('%s.csv' % event, index=False)
            df_event = pd.read_csv('%s.csv' % event)
            print(event)
            print(df_event.sort_values(by='Team', ascending=False))
            df_event.to_excel(writer, sheet_name=event, index=False)
            print()
