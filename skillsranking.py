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
print(df)
browser.close()


# urls = []
# parameters = {'event_region': 'Tennessee', 'GradeLevel': 'High School'}
#
# r = requests.post(
#    'https://www.robotevents.com/robot-competitions/vex-robotics-competition/standings/skills', data=parameters)
# print(r.text)
# r = requests.get(
#    'https://www.robotevents.com/robot-competitions/vex-robotics-competition/standings/skills')
# src = r.content
# print(src)
# soup = BeautifulSoup(src, 'lxml')
# links = soup.find_all('a')
# for link in links:
#    if "VRC" in link.text:
#        urls.append(link.attrs['href'])
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
#
# df = pd.read_html(requests.get(
#    f'{url}').content)[1].to_csv('event.csv', index=False)
