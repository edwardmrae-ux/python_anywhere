import mysql.connector
import requests
from datetime import datetime
from datetime import timedelta
import time

print('Starting...')


#print(now)

score_key = [0, 5, 4, 3, 2, 1]


a=0


for x in range(0,1):


    url = "https://golf-leaderboard-data.p.rapidapi.com/entry-list/501"
    headers = {
	    "X-RapidAPI-Host": "golf-leaderboard-data.p.rapidapi.com",
	    "X-RapidAPI-Key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8"
    }

    response = requests.request("GET", url, headers=headers)

    #print(response.text)



    json_response = response.json()
    tournament_id = json_response["results"]["tournament"]["id"]
    tournament_name = json_response["results"]["tournament"]["name"]
    entries = json_response["results"]["entry_list"]
    #print(entries)



    #Database connection
    mydb = mysql.connector.connect(
        host="erae22.mysql.pythonanywhere-services.com",
        user="erae22",
        password="7623chz2g4",
        database="erae22$golf_scores"
    )

    mycursor_tournament = mydb.cursor()
    #mycursor_leaderboard.execute("INSERT INTO leaderboard (id, name, score, position_num, status, holes_played, current_round) VALUES (%s, %s, %s, %s, %s, %s, %s)", (player_id, name, total_to_par, position, status, holes_played, current_round,))
    #mycursor_tournament.execute("TRUNCATE TABLE tournament")
    #mycursor_tournament.execute("INSERT INTO tournament (id, name) VALUES (%s, %s)" (tournament_id, tournament_name,))
    mydb.commit()


    for item in entries:
        player_id = item["player_id"]
        first_name = item["first_name"]
        last_name = item["last_name"]
        name = first_name + " " + last_name
        country = item["country"]

        mycursor_leaderboard = mydb.cursor()
        mycursor_leaderboard.execute("INSERT INTO leaderboard (id, name) VALUES (%s, %s)", (player_id, name,))
        print("Updating leaderboard")
        mydb.commit()


    mydb.close()


'''

tournament_id = json_response["results"]["tournament"]["id"]
tournament_name = json_response["results"]["tournament"]["name"]
current_round = json_response["results"]["tournament"]["live_details"]["current_round"]
tournament_status = json_response["results"]["tournament"]["live_details"]["status"]
leaderboard_updated = json_response["results"]["tournament"]["live_details"]["updated"]
leaderboard = json_response["results"]["leaderboard"]

updated_date_txt = leaderboard_updated[0:10] + " " + leaderboard_updated[11:19]
updated_date_UTC = datetime.strptime(updated_date_txt, '%Y-%m-%d %H:%M:%S')
hours = 4
hours_added = timedelta(hours = hours)
updated_date_EDT = updated_date_UTC - hours_added



mycursor_tournament = mydb.cursor()
mycursor_tournament.execute("UPDATE tournament SET id=%s, name=%s, current_round=%s, last_updated_date=%s", (tournament_id, tournament_name, current_round,updated_date_EDT,))
mydb.commit()




'''

