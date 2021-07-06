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



for bettor in bettors:
    player_list = picks[bettor]
    for player in player_list:
        mycursor_leaderboard = mydb.cursor()
        mycursor_leaderboard.execute("SELECT * FROM leaderboard WHERE name=%s", (player,))
        myresult_leaderboard = mycursor_leaderboard.fetchall()
        for x in myresult_leaderboard:
            '''print(x)'''
            player_score = x[2]*-1
            position_txt = x[3]
            position_num = x[4]
            projected_score = x[2]*-1

            if position_num == 1:
                projected_score += 5
            elif position_num == 2:
                projected_score += 4
            elif position_num == 3:
                projected_score += 3
            elif position_num == 4:
                projected_score += 2
            elif position_num == 5:
                projected_score += 1

            projected_total_score = 0


            mycursor_scores = mydb.cursor()
            mycursor_scores.execute("UPDATE scores SET player_score=%s, position=%s, projected_score=%s, projected_total_score=%s WHERE bettor=%s AND player=%s", (player_score, position_num, projected_score, projected_total_score, bettor, player,))
            mydb.commit()
            '''print(mycursor_scores.rowcount, " record(s) affected")


