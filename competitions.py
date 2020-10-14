from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

# EVENT_REGION = input('Enter the Event Region you wish to search ')
EVENT_REGION = 'South Carolina'
# GRADE_LEVEL = input('Enter grade level - "middle school" or "high school" ')
GRADE_LEVEL = 'High School'

browser = webdriver.Chrome()
browser.get('https://www.robotevents.com/robot-competitions/vex-robotics-competition?seasonId=&eventType=&name=&grade_level_id=&level_class_id=&from_date=10%2F06%2F2020&to_date=&event_region=2490&country_id=*&city=&affiliation_id=')

region = browser.find_element_by_name('event_region')
region.send_keys(f'{EVENT_REGION}')
region.send_keys(Keys.RETURN)
region.send_keys(f'{GRADE_LEVEL}')
region.send_keys(Keys.RETURN)

time.sleep(5)

df = pd.read_html(browser.page_source)
print(df)
soup = BeautifulSoup(df, 'lxml')
links = soup.find_all('a')
print(soup)
# for link in links:
#    if "VRC" in link.text:
#        urls.append(link.attrs['href'])

browser.close()
# print(df)


# r = requests.get(url)
# src = r.content
# soup = BeautifulSoup(src, 'lxml')
# links = soup.find_all('a')
# for link in links:
#    if "VRC" in link.text:
#        urls.append(link.attrs['href'])
#
# del urls[0]
# EVENT = "https://www.robotevents.com/robot-competitions/vex-robotics-competition/RE-VRC-20-2420.html#teams"
# print(urls[1])
# print(EVENT)
# r = requests.get(f'{EVENT}')
# src = r.content
# soup = BeautifulSoup(src, 'lxml')
# table = soup.find_all('table')[1]
# df = pd.read_html(str(table))
# print(df)
