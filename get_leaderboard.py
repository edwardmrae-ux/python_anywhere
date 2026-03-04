import mysql.connector
import requests
from datetime import datetime
from datetime import timedelta

url='https://golf-leaderboard-data.p.rapidapi.com/leaderboard/294'
tour_id = 2
season_id = 2021
tournament_id = 294
now = datetime.now()
'''now = datetime.strptime('2021-07-15 20:15:00', '%Y-%m-%d %H:%M:%S')'''
a=0

if now > datetime.strptime('2021-07-15 08:00:00', '%Y-%m-%d %H:%M:%S') and now < datetime.strptime('2021-07-15 19:00:00', '%Y-%m-%d %H:%M:%S'):
    a += 1
    print('not qutting')
elif now > datetime.strptime('2021-07-16 08:00:00', '%Y-%m-%d %H:%M:%S') and now < datetime.strptime('2021-07-16 19:00:00', '%Y-%m-%d %H:%M:%S'):
    a += 1
    print('not qutting')
elif now > datetime.strptime('2021-07-17 08:00:00', '%Y-%m-%d %H:%M:%S') and now < datetime.strptime('2021-07-17 18:00:00', '%Y-%m-%d %H:%M:%S'):
    a += 1
    print('not qutting')
elif now > datetime.strptime('2021-07-18 08:00:00', '%Y-%m-%d %H:%M:%S') and now < datetime.strptime('2021-07-18 18:00:00', '%Y-%m-%d %H:%M:%S'):
    a += 1
    print('not qutting')
else:
    print('quitting')
    quit()


response = requests.get(url, headers = {"x-rapidapi-key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8", "x-rapidapi-host": "golf-leaderboard-data.p.rapidapi.com"}, params = {"tournament_id": "294"})

json_response = response.json()

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


'''Database connection'''
mydb = mysql.connector.connect(
    host="erae22.mysql.pythonanywhere-services.com",
    user="erae22",
    password="7623chz2g4",
    database="erae22$golf_scores"
)


mycursor_tournament = mydb.cursor()
mycursor_tournament.execute("UPDATE tournament SET id=%s, name=%s, current_round=%s, last_updated_date=%s", (tournament_id, tournament_name, current_round,updated_date_EDT,))
mydb.commit()


for item in leaderboard:
    name = item["first_name"] + " " + item["last_name"]
    position = item["position"]
    to_par = item["total_to_par"]
    status = item["status"]
    current_round = item["current_round"]
    holes_played = item["holes_played"]

    if to_par == 'E':
        to_par = 0


    mycursor_leaderboard = mydb.cursor()
    mycursor_leaderboard.execute("UPDATE leaderboard SET score=%s, position_num=%s, status=%s, holes_played=%s, current_round=%s WHERE name=%s", (to_par, position, status, holes_played, current_round, name,))
    mydb.commit()

mydb.close()

