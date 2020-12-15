from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

EVENT_REGION = input('Enter the Event Region you wish to search ')
GRADE_LEVEL = input('Enter grade level - "middle school" or "high school" ')

browser = webdriver.Chrome()
browser.get(
    'https://www.robotevents.com/robot-competitions/vex-robotics-competition/standings/skills')

region = browser.find_element_by_name('event_region')
level = browser.find_element_by_name('grade_level')
region.send_keys(f'{EVENT_REGION}')
level.send_keys(f'{GRADE_LEVEL}')
# region.send_keys(Keys.RETURN)

time.sleep(10)

# .to_csv('skills.csv', index=False)
df = pd.read_html(browser.page_source)
df[0].to_csv('./output/%s.csv' % EVENT_REGION, index=False)
df_skills = pd.read_csv('./output/%s.csv' % EVENT_REGION)
browser.close()
print(df_skills)
