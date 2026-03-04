import mysql.connector
import requests
from datetime import datetime
from datetime import timedelta

url='https://golf-leaderboard-data.p.rapidapi.com/fixtures/2/2023'

now = datetime.now()


headers = {
	"X-RapidAPI-Host": "golf-leaderboard-data.p.rapidapi.com",
	"X-RapidAPI-Key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8"
}

response = requests.request("GET", url, headers=headers)

#response = requests.get(url, headers = {"x-rapidapi-key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8", "x-rapidapi-host": "golf-leaderboard-data.p.rapidapi.com"}, params = {"tournament_id": "294"})

#print(response.text)

json_response = response.json()

tournaments = json_response["results"]

#Database connection
mydb = mysql.connector.connect(
    host="erae22.mysql.pythonanywhere-services.com",
    user="erae22",
    password="7623chz2g4",
    database="erae22$golf_scores"
)

for item in tournaments:
    tournament_id = item["id"]
    tournament_type = item["type"]
    status = item["status"]
    name = item["name"]
    tour_id = item["tour_id"]
    location = item["country"]
    course = item["course"]
    start_date = item["start_date"]
    end_date = item["end_date"]
    season = item["season"]
    timezone = item["timezone"]

    '''
    print(tournament_id)
    print(tournament_type)
    print(status)
    print(name)
    print(tour_id)
    print(location)
    print(course)
    print(start_date)
    print(end_date)
    print(season)
    print(timezone)
    '''
    mycursor_tournaments = mydb.cursor()
    mycursor_tournaments.execute("INSERT INTO all_tournaments (id, type, status, name, tour_id, location, course, start_date, end_date, season, timezone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (tournament_id, tournament_type, status, name, tour_id, location, course, start_date, end_date, season, timezone,))
    mydb.commit()

mydb.close()

