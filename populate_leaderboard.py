import mysql.connector
import requests

url='https://golf-leaderboard-data.p.rapidapi.com/leaderboard/25?tournament_id=291'
tour_id = 2
season_id = 2021
tournament_id = 294

print("New Request... \n \n")


response = requests.get(url, headers = {"x-rapidapi-key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8", "x-rapidapi-host": "golf-leaderboard-data.p.rapidapi.com"}, params = {"tournament_id": "291"})


json_response = response.json()

tournament_id = json_response["results"]["tournament"]["id"]
tournament_name = json_response["results"]["tournament"]["name"]
current_round = json_response["results"]["tournament"]["live_details"]["current_round"]
tournament_status = json_response["results"]["tournament"]["live_details"]["status"]
leaderboard = json_response["results"]["leaderboard"]


'''Database connection'''
mydb = mysql.connector.connect(
  host="erae22.mysql.pythonanywhere-services.com",
  user="erae22",
  password="7623chz2g4",
  database="erae22$golf_scores"
)

mycursor_tournament = mydb.cursor()
mycursor_tournament.execute("INSERT INTO tournament (id, name, current_round, status) VALUES(%s, %s, %s, %s", (tournament_id, tournament_name, current_round, tournament_status,))
mydb.commit()


for item in leaderboard:
    name = item["first_name"] + " " + item["last_name"]
    position = item["position"]
    to_par = item["total_to_par"]
    status = item["status"]

    mycursor_leaderboard = mydb.cursor()
    mycursor_leaderboard.execute("INSERT INTO leaderboard (name, score, positition_num, status) VALUES (%s, 0, 0, 'active')", (name, ))
    mydb.commit()
