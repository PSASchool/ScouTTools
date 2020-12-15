import pandas as pd
import requests
import json
import csv
from pandas.io.json import json_normalize
import config  # This file contains the bearer key
import os
import numpy as np

pd.set_option('display.max_rows', None)
os.system('clear')
headers = {
    'Authorization': 'Bearer ' + config.api_userkey,
    'Content-Type': 'application/json; charset=utf-8'
}

query = {"season": 139,
         "myEvents": True,
         }


def make_dataframe(uri, query):
    df_return = pd.DataFrame()
    response = requests.get(config.api_url_base+uri,
                            headers=headers, params=query).json()
    num_pages = response['meta']['last_page']
    for page in range(1, num_pages+1):
        response = requests.get(config.api_url_base+uri + '?page=' + str(page),
                                headers=headers, params=query).json()
        norm_data = pd.json_normalize(response['data'])
        df_return = df_return.append(norm_data, ignore_index=True)
    return(df_return)


# Get list of competitions with teams related to api key owner
df_competitions = make_dataframe('events', query)
df_competitions.drop(columns=(['program.id', 'program.name', 'program.code', 'season.id', 'season.name', 'season.code', 'location.venue', 'location.address_1', 'location.address_2',
                               'location.city', 'location.postcode', 'location.country', 'location.coordinates.lat', 'location.coordinates.lon', 'divisions', 'level', 'ongoing', 'event_type']), inplace=True)
print(df_competitions)
event_list = df_competitions['id']

# Get a list of teams in each event
df_teams = pd.DataFrame()
for id in event_list:
    df_temp = make_dataframe('events/'+str(id)+'/teams', query)
    df_teams = df_teams.append(df_temp, ignore_index=True)
df_teams.drop(columns=(['program.id', 'program.name', 'program.code', 'location.venue', 'location.address_1', 'location.address_2',
                        'location.city', 'location.postcode', 'location.country', 'location.coordinates.lat', 'location.coordinates.lon', 'registered']), inplace=True)
df_teams.drop_duplicates(inplace=True)
print(df_teams)

# Get rankings for each team in list
df_ranks = pd.DataFrame()
team_list = df_teams['id']
for id in team_list:
    df_temp = make_dataframe('teams/'+str(id)+'/rankings', query)
    df_ranks = df_ranks.append(df_temp, ignore_index=True)
df_ranks.drop(columns=(['id', 'division.id', 'division.name',
                        'division.code', 'team.code']), inplace=True)
df_ranks.drop_duplicates(inplace=True)
print(df_ranks)

# Get skills rankings for each team in list
df_skills = pd.DataFrame()
for id in team_list:
    df_temp = make_dataframe('teams/'+str(id)+'/skills', query)
    df_skills = df_skills.append(df_temp, ignore_index=True)
df_skills.drop(columns=(['id',  'team.code', 'season.id',
                         'season.name', 'season.code']), inplace=True)
df_skills.drop_duplicates(inplace=True)
print(df_skills)

# Get awards won per team list

#df_awards = pd.DataFrame()
# for id in team_list:
#    df_temp = make_dataframe('teams/'+str(id)+'/awards', query)
#    df_awards = df_awards.append(df_temp, ignore_index=True)
# df_awards.drop(
#    columns=(['id', 'order', 'individualWinners', 'event.name']), inplace=True)
# print(df_awards.columns)
# print(df_awards)

with pd.ExcelWriter('./output/ScouTTool.xlsx') as writer:  # pylint: disable=abstract-class-instantiated
    df_competitions.to_excel(writer, sheet_name='Events', index=False)
    df_teams.to_excel(writer, sheet_name='Teams', index=False)
    df_ranks.to_excel(writer, sheet_name='Rankings', index=False)
    df_skills.to_excel(writer, sheet_name='Skills', index=False)
#    df_awards.to_excel(writer, sheet_name='Awards', index=False)

#team_list = df_teams['id']
# os.system('clear')
# for team in team_list:
#    print(f'######################## {team} #########################')
#    filtered = df_ranks[df_ranks['team.id'] == f'{team}']
#    rank_table = pd.pivot_table(filtered, index=['team.name']), values = ['rank', 'wins', 'losses', 'ties']
#    if not rank_table.empty:
#        print(rank_table.sort_values(by='wins', ascending=False))
#
#
#    filtered = df_skills[df_skills['season'] == f'{season}']
#    skills_table = pd.pivot_table(
#        filtered, index=['number'], values=['score'], columns=['type'], aggfunc=np.max)
#    if not skills_table.empty:
#        print('Max Skills score per Team')
#        print(skills_table)
#        print()
#
#    filtered = df_ranks[df_ranks['team.id'] == f'{team}']
#    ranks_table = pd.pivot_table(
#        filtered, index=['team.name'], values=['rank'], aggfunc=np.mean)
#    if not ranks_table.empty:
#        print('Season Average Qualifying Rank')
#        print(ranks_table.sort_values(by='rank'))
#        print()
#
#    filtered = df_results[df_results['season'] == f'{season}']
#    results_table2 = pd.pivot_table(filtered, index=['number'], values=[
#                                    'wins', 'losses', 'ties'], aggfunc=np.sum)
#    if not results_table2.empty:
#        print('Total Wins-Loss-Ties per Team')
#        print(results_table2.sort_values(by='wins', ascending=False))
#        print()
#
#    filtered = df_results[df_results['season'] == f'{season}']
#    results_table3 = pd.pivot_table(
#        filtered, index=['number'], values=['wp', 'ap', 'sp'], aggfunc=np.mean)
#    if not results_table3.empty:
#        print('Average WP-AP-SP per Team')
#        print(results_table3)
#        print()
#
#    filtered = df_results[df_results['season'] == f'{season}']
#    results_table4 = pd.pivot_table(
#        filtered, index=['number'], values=['opr', 'dpr', 'ccwm'], aggfunc=np.mean)
#    if not results_table4.empty:
#        print('Average opr-dpr-ccwm per Team')
#        print(results_table4.sort_values(by='ccwm', ascending=False))
#        print()
