import requests
from datetime import datetime
from datetime import timedelta
import mysql.connector
from time import strftime, localtime
import time

print("--------Starting---------")

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="erae22",
    password="7623chz2g4",
    hostname="erae22.mysql.pythonanywhere-services.com",
    databasename="erae22$ncaa_tourney",
)

'''Database connection'''

mydb = mysql.connector.connect(
  host="erae22.mysql.pythonanywhere-services.com",
  user="erae22",
  password="7623chz2g4",
  database="erae22$ncaa_tourney"
)

now = datetime.now()
now_EDT = now - timedelta(hours=4)

#------------------Find teams and add to teams table------------------

#Games API call
url = "https://basketapi1.p.rapidapi.com/api/basketball/tournament/13434/schedules/20/3/2025"

headers = {
	"X-RapidAPI-Key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8",
	"X-RapidAPI-Host": "basketapi1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

#print(response.text)

json_response = response.json()

#print(json_response)

games = json_response["events"]


#Looping through games
for game in games:
    tournament = game["tournament"]["name"]
    if tournament == 'NCAA Division I, Championship':
        game_id = game["id"]
        game_status = game["status"]["description"]
        epoch_start_time = game["startTimestamp"]
        game_start = strftime('%Y-%m-%d %H:%M:%S', localtime(epoch_start_time))
        #print(game_start)


        home_team_id = game["homeTeam"]["id"]
        home_team_name = game["homeTeam"]["name"]
        away_team_id = game["awayTeam"]["id"]
        away_team_name = game["awayTeam"]["name"]

        #print("Starting game: " + str(game_id) + " | " + home_team_name + " vs. " + away_team_name)

        if game_status == 'Not started':
            home_team_score = 0
            away_team_score = 0
        else:
            home_team_score = game["homeScore"]["current"]
            away_team_score = game["awayScore"]["current"]

    print(str(home_team_id) + " - " + str(home_team_name))



print("--------Finshed---------")

mydb.close()

