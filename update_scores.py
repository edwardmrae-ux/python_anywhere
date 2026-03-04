import mysql.connector

'''Database connection'''

mydb = mysql.connector.connect(
  host="erae22.mysql.pythonanywhere-services.com",
  user="erae22",
  password="7623chz2g4",
  database="erae22$golf_scores"
)

'''Bettors'''

bettors = []

mycursor_bettors = mydb.cursor()
mycursor_bettors.execute("SELECT * FROM bettors")
myresult_bettors = mycursor_bettors.fetchall()

picks = {}

for item in myresult_bettors:
    bettors.append(item[1])

for bettor in bettors:
  players = []

  mycursor_picks = mydb.cursor()
  mycursor_picks.execute("SELECT * FROM picks WHERE bettor=%s", (bettor,))
  myresult_picks = mycursor_picks.fetchall()
  for x in myresult_picks:
      players.append(x[2])
  picks[bettor] = players

mycursor_tournament = mydb.cursor()
mycursor_tournament.execute("SELECT current_round, status FROM tournament")
myresult_tournament = mycursor_tournament.fetchall()


current_round = myresult_tournament[0][0]
#tournament_status = myresult_tournament[0][1]
tournament_status = 'completed'


for bettor in bettors:
    player_list = picks[bettor]
    for player in player_list:

        mycursor_leaderboard = mydb.cursor()
        mycursor_leaderboard.execute("SELECT * FROM leaderboard WHERE name=%s", (player,))
        myresult_leaderboard = mycursor_leaderboard.fetchall()
        for x in myresult_leaderboard:

            player_score = x[2]*-1
            position_txt = x[3]
            position_num = x[4]
            status = x[5]

            position_bonus = 0
            cut_bonus = 0
            round_2_complete = True


            if position_num == 1:
                position_bonus += 5
            elif position_num == 2:
                position_bonus += 4
            elif position_num == 3:
                position_bonus += 3
            elif position_num == 4:
                position_bonus += 2
            elif position_num == 5:
                position_bonus += 1

            if status == 'active':
                cut_bonus = 5
            else:
                cut_bonus = 0

            if round_2_complete:
                player_score = player_score + cut_bonus

            if tournament_status == 'completed':
                player_score = player_score + position_bonus

            mycursor_scores = mydb.cursor()
            mycursor_scores.execute("UPDATE scores SET player_score=%s, position=%s, cut_bonus=%s, position_bonus=%s WHERE bettor=%s AND player=%s", (player_score, position_num, cut_bonus, position_bonus, bettor, player,))
            mydb.commit()

    mycursor_get_scores = mydb.cursor()
    mycursor_get_scores.execute("SELECT player_score FROM scores WHERE bettor=%s", (bettor,))
    myresult_get_scores = mycursor_get_scores.fetchall()

    score_list = []
    for score in myresult_get_scores:
        score_list.append(score[0])

    #print(bettor)
    #print(score_list)
    score_list.remove(min(score_list))
    #print(score_list)

    total_score = 0
    for score in score_list:
        total_score += score


    mycursor_update_bettor_scores = mydb.cursor()
    mycursor_update_bettor_scores.execute("UPDATE bettor_scores SET current_Score=%s WHERE bettor=%s", (total_score, bettor,))
    mydb.commit()
    '''print(bettor + "'s scores updated in DB")'''


