import requests
from datetime import datetime
from datetime import timedelta
import mysql.connector
from time import strftime, localtime

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

mycursor_existing_teams = mydb.cursor()
mycursor_existing_teams.execute("select id from ncaa_teams")
myresult_existing_teams = mycursor_existing_teams.fetchall()


existing_teams = []
for item in myresult_existing_teams:
    existing_teams.append(item[0])
    #print(item[0])


#Games API call
url = "https://basketapi1.p.rapidapi.com/api/basketball/matches/22/3/2024"

headers = {
	"X-RapidAPI-Key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8",
	"X-RapidAPI-Host": "basketapi1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)
json_response = response.json()
games = json_response["events"]
#print(games)

teams = []

#Looping through games
for game in games:
    tournament = game["tournament"]["name"]
    #print(tournament)
    if tournament == 'NCAA Division I, Championship':
        game_id = game["id"]
        home_team_id = game["homeTeam"]["id"]
        home_team_name = game["homeTeam"]["name"]
        away_team_id = game["awayTeam"]["id"]
        away_team_name = game["awayTeam"]["name"]

        home_dict = {"id":home_team_id, "name":home_team_name}
        away_dict = {"id":away_team_id, "name":away_team_name}

        teams.append(home_dict)
        teams.append(away_dict)


print(teams)




for team in teams:
    team_id = team["id"]
    team_name = team["name"]

    mycursor_teams = mydb.cursor()

    if team_id not in existing_teams:
        mycursor_teams.execute("INSERT INTO ncaa_teams (id, name) VALUES (%s, %s)", (team_id, team_name ))

    mydb.commit()


print("all done")

mydb.close()

