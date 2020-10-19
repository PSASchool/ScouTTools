# TeamRanking
[note] vexdb.io does not have current year data so i had to switch to scraping websites
with selenium and beautifulsoup.

## competitions.py
Competitions.py will ask for "Event Region", "Grade Level" and "Season"
(currently set to "South Carolina", "High School" and "Change up" respectively for testing purposes)
It will then create tables of the teams registered for the events and save them to an 
excel spreadsheet to be used for scouting and such.

## skillsrank.py
Skillsrank.py will ask for "Event Region" and "Grade Level" and create a table of
the regions skillsrank page.  If you leave either filed blank, you will get all
regions or grade levels.

## teamranker.py (won't work without vexdb.io)
Teamranker.py will take a given tournament and produce a ranked list based on vexdb.io
stats for current year.  The goal will be to use the output of competitions to give
predictive rankings for each team in the event entered at the beginning of the program.
Maybe through in some probablilties with some graphs and stuff.
