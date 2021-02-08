import csv
import os
import requests
import json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import config  # This file contains the bearer key

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
canceled = df_competitions[df_competitions['sku']
                           == 'RE-VRC-20-2659'].index  # Event was canceled
df_competitions.drop(canceled, inplace=True)
print(df_competitions)

event_list = df_competitions['id']
finalized = df_competitions[df_competitions['awards_finalized'] == True].index
df_upcomming = df_competitions.drop(finalized)
future_events = df_upcomming['id']

# Get a list of teams in each event
df_teams = pd.DataFrame()
for id in event_list:
    df_temp = make_dataframe('events/'+str(id)+'/teams', query)
    df_teams = df_teams.append(df_temp, ignore_index=True)
    name = str(id)
#    df_name = df_temp
#    df_name.drop(columns=(['program.id', 'program.name', 'program.code', 'location.venue', 'location.address_1', 'location.address_2',
#                           'location.city', 'location.postcode', 'location.country', 'location.coordinates.lat', 'location.coordinates.lon', 'registered']), inplace=True)
#    print(df_name)

df_teams.drop(columns=(['program.id', 'program.name', 'program.code', 'location.venue', 'location.address_1', 'location.address_2',
                        'location.city', 'location.postcode', 'location.country', 'location.coordinates.lat', 'location.coordinates.lon', 'registered']), inplace=True)
df_teams.drop_duplicates(inplace=True)
# print(df_teams)

# Get rankings for each team in list
df_ranks = pd.DataFrame()
team_list = df_teams['id']
for id in team_list:
    df_temp = make_dataframe('teams/'+str(id)+'/rankings', query)
    df_ranks = df_ranks.append(df_temp, ignore_index=True)
df_ranks.drop(columns=(['id', 'division.id', 'division.name',
                        'division.code', 'team.code']), inplace=True)
df_ranks.drop_duplicates(inplace=True)
df_rank_tot = df_ranks.groupby(['team.id']).agg(
    {'wins': 'sum', 'losses': 'sum', 'ties': 'sum'})
# print(df_ranks)

# Get skills rankings for each team in list
df_skills = pd.DataFrame()
for id in team_list:
    df_temp = make_dataframe('teams/'+str(id)+'/skills', query)
    df_skills = df_skills.append(df_temp, ignore_index=True)
df_skills.drop(columns=(['id', 'rank', 'team.code', 'season.id',
                         'season.name', 'season.code']), inplace=True)
df_skills.drop_duplicates(inplace=True)
skills_grp = df_skills.groupby(['team.id', 'type']).agg({'score': 'max'})
ustk_skills = skills_grp.unstack('type', fill_value=0)

# Get awards won per team list
# df_awards = pd.DataFrame()
# for id in team_list:
#    df_temp = make_dataframe('teams/'+str(id)+'/awards', query)
#    df_awards = df_awards.append(df_temp, ignore_index=True)
# df_awards.drop(
# columns=(['id', 'order', 'individualWinners', 'event.name']), inplace=True)
# print(df_awards.columns)
# print(df_awards)

with pd.ExcelWriter('./output/ScouTTool.xlsx') as writer:  # pylint: disable=abstract-class-instantiated
    for id in future_events:
        df_temp = make_dataframe('events/'+str(id)+'/teams', query)
        name = str(id)
        df_temp.drop(columns=(['robot_name', 'organization', 'grade', 'location.region', 'program.id', 'program.name', 'program.code', 'location.venue', 'location.address_1', 'location.address_2',
                               'location.city', 'location.postcode', 'location.country', 'location.coordinates.lat', 'location.coordinates.lon', 'registered']), inplace=True)
        step_1 = pd.merge(df_temp, df_rank_tot,
                          left_on='id', right_on='team.id')
        result = pd.merge(step_1, ustk_skills,
                          left_on='id', right_on='team.id')
        result.sort_values(by='wins', ascending=False, inplace=True)
        print(name)
        print(result)
        print()
        result.to_excel(writer, sheet_name=name, index=False)
    df_competitions.to_excel(writer, sheet_name='Events', index=False)
    df_teams.to_excel(writer, sheet_name='Teams', index=False)
    df_ranks.to_excel(writer, sheet_name='Rankings', index=False)
    df_skills.to_excel(writer, sheet_name='Skills', index=False)
#    df_awards.to_excel(writer, sheet_name='Awards', index=False)


#    df_awards.to_excel(writer, sheet_name='Awards', index=False)

#from trueskill import Rating
#from trueskill.mathematics import cdf
#
# def Pwin(rA=Rating(), rB=Rating()):
#    deltaMu = rA.mu - rB.mu
#    rsss = sqrt(rA.sigma**2 + rB.sigma**2)
#    return cdf(deltaMu/rsss)
#
# def Pwin(rAlist=[Rating()],  rBlist=[Rating()]):
#    deltaMu = sum( [x.mu for x in rAlist])  - sum( [x.mu for x in  rBlist])
#    rsss = sqrt(sum( [x.sigma**2 for x in  rAlist]) + sum( [x.sigma**2 for x in rBlist]) )
#    return cdf(deltaMu/rsss)
