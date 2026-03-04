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

#returning games already in table and finished games

mycursor_existing_games = mydb.cursor()
mycursor_existing_games.execute("select id, status from ncaa_games")
myresult_existing_games = mycursor_existing_games.fetchall()


existing_games = []
finished_games = []
for item in myresult_existing_games:
    existing_games.append(item[0])

    if item[1] == 'Ended' or item[1] == 'AET':
        finished_games.append(item[0])

#print("Finished games:")
#print(finished_games)


#Games API call
url = "https://basketapi1.p.rapidapi.com/api/basketball/matches/20/3/2025"

headers = {
	"X-RapidAPI-Key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8",
	"X-RapidAPI-Host": "basketapi1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

#print(response.text)

json_response = response.json()

#print(json_response)

games = json_response["events"]



#print("games:")
#print(games)


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

        #game_id = str(id)+"_"+str(home_team_id)
        #print(str(id) + " - " + str(tournament))



        #game_date_response = game["date"]
        #date_size = len(game_date_response)
        #trimmed_game_date = game_date_response[:date_size - 6]
        #print(date)
        date_format_str = "%Y-%m-%d %H:%M:%S"

        game_time_date = datetime.strptime(game_start, date_format_str)

        game_date = game_time_date - timedelta(hours=4)

        game_round = 0
        if(game_date > datetime.strptime('2025-03-20', "%Y-%m-%d") and game_date < datetime.strptime('2025-03-22', "%Y-%m-%d")):
            game_round = 1
        elif(game_date > datetime.strptime('2025-03-22', "%Y-%m-%d") and game_date < datetime.strptime('2025-03-24', "%Y-%m-%d")):
            game_round = 2
        elif(game_date > datetime.strptime('2025-03-27', "%Y-%m-%d") and game_date < datetime.strptime('2025-03-29', "%Y-%m-%d")):
            game_round = 3
        elif(game_date > datetime.strptime('2025-03-29', "%Y-%m-%d") and game_date < datetime.strptime('2025-03-31', "%Y-%m-%d")):
            game_round = 4
        elif(game_date > datetime.strptime('2025-04-05', "%Y-%m-%d") and game_date < datetime.strptime('2025-04-06', "%Y-%m-%d")):
            game_round = 5
        elif(game_date > datetime.strptime('2025-04-07', "%Y-%m-%d") and game_date < datetime.strptime('2025-04-08', "%Y-%m-%d")):
            game_round = 6

        game_complete = 0

        if game_status == 'Ended' or game_status == 'AET':
            game_complete = 1
            if home_team_score > away_team_score:
                game_winner = home_team_id
            else:
                game_winner = away_team_id
        else:
            game_winner = None

        mycursor_games = mydb.cursor()

        if game_id in existing_games and game_id != 156679:
            mycursor_games.execute("UPDATE ncaa_games SET home_score = %s, away_score = %s, status = %s, winner = %s, last_updated = %s WHERE id = %s", (home_team_score, away_team_score, game_status, game_winner, now_EDT, game_id,  ))
            #print("updating: ", id)
            #print(id)

            if game_id not in finished_games and game_complete == 1:

                #home team updates
                if home_team_id == game_winner:
                    mycursor_games.execute("UPDATE ncaa_teams SET alive = 1, wins = %s WHERE id = %s", (game_round, home_team_id, ))
                else:
                    num_wins = game_round - 1
                    mycursor_games.execute("UPDATE ncaa_teams SET alive = 0, wins = %s, exit_round = %s WHERE id = %s", (num_wins, game_round, home_team_id, ))

                #away team updates
                if away_team_id == game_winner:
                    mycursor_games.execute("UPDATE ncaa_teams SET alive = 1, wins = %s WHERE id = %s", (game_round, away_team_id, ))
                else:
                    num_wins = game_round - 1
                    mycursor_games.execute("UPDATE ncaa_teams SET alive = 0, wins = %s, exit_round = %s WHERE id = %s", (num_wins, game_round, away_team_id, ))

            #mydb.commit()
        elif id != 156679:
            mycursor_games.execute("INSERT INTO ncaa_games (id, date, home, away, home_score, away_score, status, round, last_updated, home_name, away_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )", (game_id, game_date, home_team_id, away_team_id, home_team_score, away_team_score, game_status, game_round, now_EDT, home_team_name, away_team_name ))
            #print("inserting", id, game_date, home_team_id, away_team_id, home_score, away_score, game_status, game_round, home_team_name, away_team_name)
        mydb.commit()

        #print("finished game: " + str(game_id))



'''-----------------------------------Update team scores '''

print("starting updating team scores section")

'''Database connection'''


#returning games already in table and finished games

mycursor_teams = mydb.cursor()
mycursor_teams.execute("select id, seed, wins from ncaa_teams")
myresult_teams = mycursor_teams.fetchall()


for item in myresult_teams:
    team_id = item[0]
    seed = item[1]
    wins = item[2]

    #print("Team: " + str(team_id) + "," + str(seed) + "," + str(wins))

    points = seed * wins

    mycursor_update_teams = mydb.cursor()
    mycursor_update_teams.execute("update ncaa_teams set points = %s WHERE id = %s", (points, team_id, ))
    mydb.commit()


print("finished updating team scores section")

'''-----------------------------------Update leaderboard'''

print("starting updating leaderboard section")



#returning games already in table and finished games

mycursor_teams = mydb.cursor()
mycursor_teams.execute("select id, points from ncaa_teams")
myresult_teams = mycursor_teams.fetchall()


team_score_data = {}

for item in myresult_teams:
    team_id = item[0]
    points = item[1]

    team_score_data[team_id] = points

#print(team_score_data)


mycursor_picks = mydb.cursor()
mycursor_picks.execute("select id, name, pick1_id, pick2_id, pick3_id, pick4_id, pick5_id from ncaa_picks")
myresult_picks = mycursor_picks.fetchall()

print(myresult_picks)


for item in myresult_picks:
    player_id = item[0]
    player_name = item[1]
    pick1_id = item[2]
    pick2_id = item[3]
    pick3_id = item[4]
    pick4_id = item[5]
    pick5_id = item[6]

    pick1_pts = team_score_data[pick1_id]
    pick2_pts = team_score_data[pick2_id]
    pick3_pts = team_score_data[pick3_id]
    pick4_pts = team_score_data[pick4_id]
    pick5_pts = team_score_data[pick5_id]

    total_points = pick1_pts + pick2_pts + pick3_pts + pick4_pts + pick5_pts

    #print(player_name, ": ", pick1_pts, ",", pick1_pts, ",", pick1_pts,",", pick1_pts,",", pick1_pts, ";", total_points)


    mycursor_update_picks = mydb.cursor()
    mycursor_update_picks.execute("update ncaa_picks set pick1_pts = %s, pick2_pts = %s, pick3_pts = %s, pick4_pts = %s, pick5_pts = %s, total_pts = %s WHERE id = %s", (pick1_pts, pick2_pts, pick3_pts, pick4_pts, pick5_pts, total_points, player_id, ))
    mydb.commit()


print("finished updating leaderboard section")
print("finished everything")

#print('Sleeping for 5 seconds')
#time.sleep(5)




mydb.close()

