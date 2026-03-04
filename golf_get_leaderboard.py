import mysql.connector
import requests
from datetime import datetime
from datetime import timedelta
import time

print('Starting...')


#print(now)

score_key = [0, 5, 4, 3, 2, 1]


a=0


for x in range(0,30):
    now = datetime.now()
    now_EDT = now - timedelta(hours=4)
    #now = datetime.strptime('2022-04-09 14:25:00', '%Y-%m-%d %H:%M:%S')
    print("Starting loop: " + str(x))
    print(now_EDT)

    if now_EDT > datetime.strptime('2023-04-06 08:00:00', '%Y-%m-%d %H:%M:%S') and now_EDT < datetime.strptime('2023-04-06 19:00:00', '%Y-%m-%d %H:%M:%S'):
        a += 1
        print('not quitting')
    elif now_EDT > datetime.strptime('2023-04-07 08:00:00', '%Y-%m-%d %H:%M:%S') and now_EDT < datetime.strptime('2023-04-07 19:00:00', '%Y-%m-%d %H:%M:%S'):
        a += 1
        print('not quitting')
    elif now_EDT > datetime.strptime('2023-04-08 09:00:00', '%Y-%m-%d %H:%M:%S') and now_EDT < datetime.strptime('2023-04-08 19:00:00', '%Y-%m-%d %H:%M:%S'):
        a += 1
        print('not quitting')
    elif now_EDT > datetime.strptime('2023-04-09 10:00:00', '%Y-%m-%d %H:%M:%S') and now_EDT < datetime.strptime('2023-04-09 19:00:00', '%Y-%m-%d %H:%M:%S'):
        a += 1
        print('not quitting')
    else:
        print('quitting')
        time.sleep(117)
        quit()




    url = "https://golf-leaderboard-data.p.rapidapi.com/leaderboard/501"
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

    #-------Date fixes---------
    date_size = len(tournament_updated)
    trimmed_updated_date = tournament_updated[:date_size - 6]
    date_format_str = "%Y-%m-%dT%H:%M:%S"
    last_updated_date = datetime.strptime(trimmed_updated_date, date_format_str)
    updated_date_EDT = last_updated_date - timedelta(hours=4)



    #Database connection
    mydb = mysql.connector.connect(
        host="erae22.mysql.pythonanywhere-services.com",
        user="erae22",
        password="7623chz2g4",
        database="erae22$golf_scores"
    )

    mycursor_tournament = mydb.cursor()
    #mycursor_leaderboard.execute("INSERT INTO leaderboard (id, name, score, position_num, status, holes_played, current_round) VALUES (%s, %s, %s, %s, %s, %s, %s)", (player_id, name, total_to_par, position, status, holes_played, current_round,))
    mycursor_tournament.execute("UPDATE tournament SET current_round=%s, last_updated_date=%s WHERE id=%s", (tournament_round, updated_date_EDT, tournament_id,))
    mydb.commit()


    for item in leaderboard:
        player_id = item["player_id"]
        first_name = item["first_name"]
        last_name = item["last_name"]
        name = first_name + " " + last_name
        position = item["position"]
        country = item["country"]
        current_round = item["current_round"]
        holes_played = item["holes_played"]
        strokes = item["strokes"]
        total_to_par = item["total_to_par"]
        status = item["status"]
        updated = item["updated"]

        if len(status) == 0:
            status = "active"

        mycursor_leaderboard = mydb.cursor()
        #mycursor_leaderboard.execute("INSERT INTO leaderboard (id, name, score, position_num, status, holes_played, current_round) VALUES (%s, %s, %s, %s, %s, %s, %s)", (player_id, name, total_to_par, position, status, holes_played, current_round,))
        if status == 'active':
            mycursor_leaderboard.execute("UPDATE leaderboard SET score=%s, position_num=%s, status=%s, holes_played=%s, current_round=%s WHERE id=%s", (total_to_par, position, status, holes_played, current_round, player_id,))
        else:
            mycursor_leaderboard.execute("UPDATE leaderboard SET position_num=%s, status=%s, holes_played=%s, current_round=%s WHERE id=%s", (position, status, holes_played, current_round, player_id,))
        mydb.commit()

        #print("Updating leaderboard")



    mycursor_picks = mydb.cursor()
    mycursor_picks.execute("select bettor, pick1_id, pick2_id, pick3_id, pick4_id, pick5_id from picks")
    myresult_picks = mycursor_picks.fetchall()



    for item in myresult_picks:
        bettor = item[0]
        pick1 = item[1]
        pick2 = item[2]
        pick3 = item[3]
        pick4 = item[4]
        pick5 = item[5]
        #print(bettor)

        bettor_total_pts = []


        #------pick1 updates---------------------------------------------
        mycursor_pick1_scores = mydb.cursor()
        mycursor_pick1_scores.execute("SELECT id, position_num, status, current_round, holes_played, score FROM leaderboard WHERE id = %s", (pick1, ))
        myresult_pick1_score = mycursor_pick1_scores.fetchall()

        pick1_position = myresult_pick1_score[0][1]
        pick1_status = myresult_pick1_score[0][2]
        pick1_round = myresult_pick1_score[0][3]
        #pick1_holes_played = myresult_pick1_score[0][4]
        pick1_to_par = myresult_pick1_score[0][5]
        pick1_pts = 0

        if pick1_position is None:
            pick1_position = 100
        if pick1_to_par is None:
            pick1_to_par = 0
        if pick1_round is None:
            pick1_round = 0

        if pick1_position < 6:
            pick1_pos_score = score_key[pick1_position]
            pick1_to_par_score = pick1_to_par * -1
            pick1_pts = pick1_pos_score + pick1_to_par_score
        else:
            pick1_pts = pick1_to_par * -1

        if pick1_round > 2 and pick1_status == 'active':
            pick1_pts += 12
        else:
            pick1_pts += 0

        bettor_total_pts.append(pick1_pts)

        #print("Pick 1 scores: " + str(pick1_pts))

        #------pick2 updates---------------------------------------------
        mycursor_pick2_scores = mydb.cursor()
        mycursor_pick2_scores.execute("SELECT id, position_num, status, current_round, holes_played, score FROM leaderboard WHERE id = %s", (pick2, ))
        myresult_pick2_score = mycursor_pick2_scores.fetchall()

        pick2_position = myresult_pick2_score[0][1]
        pick2_status = myresult_pick2_score[0][2]
        pick2_round = myresult_pick2_score[0][3]
        #pick2_holes_played = myresult_pick2_score[0][4]
        pick2_to_par = myresult_pick2_score[0][5]
        pick2_pts = 0

        if pick2_position is None:
            pick2_position = 100
        if pick2_to_par is None:
            pick2_to_par = 0
        if pick2_round is None:
            pick2_round = 0


        if pick2_position < 6:
            pick2_pos_score = score_key[pick2_position]
            pick2_to_par_score = pick2_to_par * -1
            pick2_pts = pick2_pos_score + pick2_to_par_score
        else:
            pick2_pts = pick2_to_par * -1

        if pick2_round > 2 and pick2_status == 'active':
            pick2_pts += 12
        else:
            pick2_pts += 0

        bettor_total_pts.append(pick2_pts)

        #print("Pick 2 scores: " + str(pick2_pts))

        #------pick3 updates---------------------------------------------
        mycursor_pick3_scores = mydb.cursor()
        mycursor_pick3_scores.execute("SELECT id, position_num, status, current_round, holes_played, score FROM leaderboard WHERE id = %s", (pick3, ))
        myresult_pick3_score = mycursor_pick3_scores.fetchall()

        pick3_position = myresult_pick3_score[0][1]
        pick3_status = myresult_pick3_score[0][2]
        pick3_round = myresult_pick3_score[0][3]
        #pick3_holes_played = myresult_pick3_score[0][4]
        pick3_to_par = myresult_pick3_score[0][5]

        if pick3_position is None:
            pick3_position = 100
        if pick3_to_par is None:
            pick3_to_par = 0
        if pick3_round is None:
            pick3_round = 0

        pick3_pts = 0

        print(pick3_position)

        if pick3_position < 6:
            pick3_pos_score = score_key[pick3_position]
            pick3_to_par_score = pick3_to_par * -1
            pick3_pts = pick3_pos_score + pick3_to_par_score
        else:
            pick3_pts = pick3_to_par * -1

        if pick3_round > 2 and pick3_status == 'active':
            pick3_pts += 12
        else:
            pick3_pts += 0

        bettor_total_pts.append(pick3_pts)

        #print("Pick 3 scores: " + str(pick3_pts))

        #------pick4 updates---------------------------------------------
        mycursor_pick4_scores = mydb.cursor()
        mycursor_pick4_scores.execute("SELECT id, position_num, status, current_round, holes_played, score FROM leaderboard WHERE id = %s", (pick4, ))
        myresult_pick4_score = mycursor_pick4_scores.fetchall()

        pick4_position = myresult_pick4_score[0][1]
        pick4_status = myresult_pick4_score[0][2]
        pick4_round = myresult_pick4_score[0][3]
        #pick4_holes_played = myresult_pick4_score[0][4]
        pick4_to_par = myresult_pick4_score[0][5]
        pick4_pts = 0

        if pick4_position is None:
            pick4_position = 100
        if pick4_to_par is None:
            pick4_to_par = 0
        if pick4_round is None:
            pick4_round = 0

        if pick4_position < 6:
            pick4_pos_score = score_key[pick4_position]
            pick4_to_par_score = pick4_to_par * -1
            pick4_pts = pick4_pos_score + pick4_to_par_score
        else:
            pick4_pts = pick4_to_par * -1

        if pick4_round > 2 and pick4_status == 'active':
            pick4_pts += 12
        else:
            pick4_pts += 0

        bettor_total_pts.append(pick4_pts)

        #print("Pick 4 scores: " + str(pick4_pts))

        #------pick5 updates---------------------------------------------
        mycursor_pick5_scores = mydb.cursor()
        mycursor_pick5_scores.execute("SELECT id, position_num, status, current_round, holes_played, score FROM leaderboard WHERE id = %s", (pick5, ))
        myresult_pick5_score = mycursor_pick5_scores.fetchall()

        pick5_position = myresult_pick5_score[0][1]
        pick5_status = myresult_pick5_score[0][2]
        pick5_round = myresult_pick5_score[0][3]
        #pick5_holes_played = myresult_pick5_score[0][4]
        pick5_to_par = myresult_pick5_score[0][5]
        pick5_pts = 0

        if pick5_position is None:
            pick5_position = 100
        if pick5_to_par is None:
            pick5_to_par = 0
        if pick5_round is None:
            pick5_round = 0

        if pick5_position < 6:
            pick5_pos_score = score_key[pick5_position]
            pick5_to_par_score = pick5_to_par * -1
            pick5_pts = pick5_pos_score + pick5_to_par_score
        else:
            pick5_pts = pick5_to_par * -1

        if pick5_round > 2 and pick5_status == 'active':
            pick5_pts += 12
        else:
            pick5_pts += 0

        #bettor_total_pts.append(pick5_pts)

        #print("Pick 5 scores: " + str(pick5_pts))


        #print(bettor_total_pts)
        #lowest_score = min(bettor_total_pts)
        #print(lowest_score)
        #bettor_total_pts.remove(min(bettor_total_pts))

        total_pts = sum(bettor_total_pts)
        #print(total_pts)


        #lowest_score_dict = {
        #    pick1 : pick1_pts,
        #    pick2 : pick2_pts,
        #    pick3 : pick3_pts,
        #    pick4 : pick4_pts,
        #    pick5 : pick5_pts,
        #}

        #lowest_score_dict_keys = list(lowest_score_dict.keys())
        #lowest_score_dict_values = list(lowest_score_dict.values())

        #print(lowest_score_dict_keys)
        #print(lowest_score_dict_values)

        #drop_index = lowest_score_dict_values.index(lowest_score)
        #drop_player = lowest_score_dict_keys[drop_index]
        #print(drop_index)
        #print(drop_player)

        mycursor_upate_pick_scores = mydb.cursor()
        mycursor_upate_pick_scores.execute("UPDATE picks SET pick1_pts=%s, pick2_pts=%s, pick3_pts=%s, pick4_pts=%s, pick5_pts=%s, total_pts=%s WHERE bettor=%s", (pick1_pts, pick2_pts, pick3_pts, pick4_pts, pick5_pts, total_pts, bettor,))
        mydb.commit()


    mydb.close()

    print('Sleeping for 117 seconds')
    time.sleep(117)

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

