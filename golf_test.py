import mysql.connector
import requests
from datetime import datetime
from datetime import timedelta
import time

print('Starting...')


#print(now)

score_key = [0, 5, 4, 3, 2, 1]


a=0

url = "https://golf-leaderboard-data.p.rapidapi.com/leaderboard/456"
headers = {
    "X-RapidAPI-Host": "golf-leaderboard-data.p.rapidapi.com",
    "X-RapidAPI-Key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8"
}

response = requests.request("GET", url, headers=headers)

#print(response.text)



json_response = response.json()
tournament_id = json_response["results"]["tournament"]["id"]
tournament_round = json_response["results"]["tournament"]["live_details"]["current_round"]
tournament_cut_line = json_response["results"]["tournament"]["live_details"]["cut_value"]
tournament_updated = json_response["results"]["tournament"]["live_details"]["updated"]
leaderboard = json_response["results"]["leaderboard"]

print(tournament_updated)

date_size = len(tournament_updated)
trimmed_updated_date = tournament_updated[:date_size - 6]

date_format_str = "%Y-%m-%dT%H:%M:%S"
last_updated_date = datetime.strptime(trimmed_updated_date, date_format_str)

print(last_updated_date)

updated_date_EDT = last_updated_date - timedelta(hours=4)

print(updated_date_EDT)






