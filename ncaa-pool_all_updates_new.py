import requests
from datetime import datetime
from datetime import timedelta
import mysql.connector
from time import strftime, localtime
import time

import config
from ncaa_rounds import get_round_from_date

print("--------Starting---------")

for x in range(0, 360):
    print("Starting loop: " + str(x))

    params = config.get_mysql_connection_params()
    mydb = mysql.connector.connect(**params)

    now = datetime.now()
    now_EDT = now - timedelta(hours=4)
    current_day = now.day
    current_month = now.month
    current_year = now.year

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

    print("existing games: " + str(existing_games))
    print("finished games: " + str(finished_games))

    #print("Finished games:")
    #print(finished_games)


    url = f"{config.RAPIDAPI_BASE_URL}/api/basketball/matches/{current_day}/{current_month}/{current_year}"
    headers = config.get_rapidapi_headers()
    response = requests.request("GET", url, headers=headers)

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
            game_round = get_round_from_date(game_date)

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
            elif game_id != 156679:
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

    #print("myresult teams: " + str(myresult_teams))

    for item in myresult_teams:
        team_id = item[0]
        seed = item[1]
        wins = item[2]

        points = seed * wins

        #print("team id: " + str(team_id) + ". seed: " + str(seed) + ". wins: " + str(wins) + ". points: " + str(points) + ".")

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

    #print(myresult_picks)


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

    try:
        import ncaa_box_pool_scores
        ncaa_box_pool_scores.run()
        print("box pool scores updated")
    except Exception as e:
        print("box pool scores error:", e)

    print("finished everything")
    mydb.close()
    time.sleep(10)

