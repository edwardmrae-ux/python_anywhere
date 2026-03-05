# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from operator import itemgetter

import config
from ncaa_rounds import get_current_round

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "change-me-in-production"

app.config["SQLALCHEMY_DATABASE_URI"] = config.get_sqlalchemy_uri()
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/ncaa", methods=["GET", "POST"])
def index_ncaa():
    params = config.get_mysql_connection_params()
    mydb = mysql.connector.connect(**params)

    mycursor_player_leaderboard = mydb.cursor()
    mycursor_player_leaderboard.execute("select p.id,p.name,p.pick1_id,p.pick1_name,p.pick2_id,p.pick2_name,p.pick3_id,p.pick3_name,p.pick4_id,p.pick4_name,p.pick5_id,p.pick5_name,p.pick1_pts,p.pick2_pts,p.pick3_pts,p.pick4_pts,p.pick5_pts,p.total_pts from ncaa_picks p")
    myresult_player_leaderboard = mycursor_player_leaderboard.fetchall()

    mycursor_teams = mydb.cursor()
    mycursor_teams.execute("select * from ncaa_teams")
    myresult_teams = mycursor_teams.fetchall()

    mydb.close()

    current_round = get_current_round()

    scores = []
    for item in myresult_player_leaderboard:
        player_id = item[0]
        name = item[1]
        pick1_id = item[2]
        pick1_name = item[3]
        pick2_id = item[4]
        pick2_name = item[5]
        pick3_id = item[6]
        pick3_name = item[7]
        pick4_id = item[8]
        pick4_name = item[9]
        pick5_id = item[10]
        pick5_name = item[11]
        pick1_pts = item[12]
        pick2_pts = item[13]
        pick3_pts = item[14]
        pick4_pts = item[15]
        pick5_pts = item[16]
        total_pts = item[17]

        scores.append([player_id,name,pick1_id,pick1_name,pick2_id,pick2_name,pick3_id,pick3_name,pick4_id,pick4_name,pick5_id,pick5_name,pick1_pts,pick2_pts,pick3_pts,pick4_pts,pick5_pts,total_pts])

    scores = sorted(scores, key=itemgetter(17), reverse=True)

    team_alive_data = {}
    team_seed_data = {}
    team_win_data = {}
    team_points_data = {}
    for item in myresult_teams:
        team_id = item[0]
        team_name = item[1]
        seed = item[2]
        alive = item[3]
        wins = item[4]
        exit_round = item[5]
        points = item[6]
        short_name = item[8]

        team_alive_data[short_name] = alive
        team_seed_data[short_name] = seed
        team_win_data[short_name] = wins
        team_points_data[short_name] = points

    if request.method == "GET":
        return render_template("ncaa-pool_newAPI.html", scores=scores, team_alive_data=team_alive_data, team_seed_data=team_seed_data, team_win_data=team_win_data, team_points_data=team_points_data, current_round=current_round)
        #return render_template("hello_world.html")


@app.route("/golf", methods=["GET", "POST"])
def index_golf():

    mydb = mysql.connector.connect(
        host="erae22.mysql.pythonanywhere-services.com",
        user="erae22",
        password="7623chz2g4",
        database="erae22$golf_scores"
    )

    mycursor_picks = mydb.cursor()
    mycursor_picks.execute("select bettor, pick1_id, pick2_id, pick3_id, pick4_id, pick5_id, pick1_pts, pick2_pts, pick3_pts, pick4_pts, pick5_pts, total_pts, dropped_player from picks")
    myresult_picks = mycursor_picks.fetchall()

    mycursor_leaderboard = mydb.cursor()
    mycursor_leaderboard.execute("select id, name, score, position_num, status, holes_played, current_round from leaderboard")
    myresult_leaderboard = mycursor_leaderboard.fetchall()

    mycursor_tournament = mydb.cursor()
    mycursor_tournament.execute("select current_round, last_updated_date from tournament")
    myresult_tournament = mycursor_tournament.fetchall()

    mydb.close()

    tournament_round = myresult_tournament[0][0]
    tournament_updated = myresult_tournament[0][1]

    #print(myresult_leaderboard)

    picks_scores = []
    for item in myresult_picks:
        bettor = item[0]
        pick1_id = item[1]
        pick2_id = item[2]
        pick3_id = item[3]
        pick4_id = item[4]
        pick5_id = item[5]
        pick1_pts = item[6]
        pick2_pts = item[7]
        pick3_pts = item[8]
        pick4_pts = item[9]
        pick5_pts = item[10]
        total_pts = item[11]
        dropped_player = item[12]

        picks_scores.append([bettor, pick1_id, pick2_id, pick3_id, pick4_id, pick5_id, pick1_pts, pick2_pts, pick3_pts, pick4_pts, pick5_pts, total_pts, dropped_player])

    picks_scores = sorted(picks_scores, key=itemgetter(11), reverse=True)

    player_name_data = {}
    player_score_data = {}
    player_position_data = {}
    player_status_data = {}
    player_holes_played_data = {}
    player_current_round_data = {}
    for item in myresult_leaderboard:
        player_id = item[0]
        player_name = item[1]
        player_score = item[2]
        player_position = item[3]
        player_status = item[4]
        player_holes_played = item[5]
        player_current_round = item[6]


        player_name_data[player_id] = player_name
        player_score_data[player_id] = player_score
        player_position_data[player_id] = player_position
        player_status_data[player_id] = player_status
        player_holes_played_data[player_id] = player_holes_played
        player_current_round_data[player_id] = player_current_round



    if request.method == "GET":
        return render_template("golf_pool.html", picks_scores=picks_scores, player_name_data=player_name_data, player_score_data=player_score_data, player_position_data=player_position_data, player_status_data=player_status_data, player_holes_played_data=player_holes_played_data, tournament_round=tournament_round, tournament_updated=tournament_updated)


@app.route("/ncaa-box-pool", methods=["GET", "POST"])
def ncaa_box_pool():
    """NCAA March Madness box pool: leaderboard and admin form to add participants."""
    params = config.get_mysql_connection_params()
    mydb = mysql.connector.connect(**params)

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        row_digit = request.form.get("row_digit")
        col_digit = request.form.get("col_digit")
        try:
            row_digit = int(row_digit) if row_digit is not None else None
            col_digit = int(col_digit) if col_digit is not None else None
        except (TypeError, ValueError):
            row_digit = col_digit = None
        if name and row_digit is not None and col_digit is not None and 0 <= row_digit <= 9 and 0 <= col_digit <= 9:
            cur = mydb.cursor()
            try:
                cur.execute(
                    "INSERT INTO box_pool_participants (name, row_digit, col_digit, total_points, games_won) VALUES (%s, %s, %s, 0, 0)",
                    (name, row_digit, col_digit)
                )
                mydb.commit()
                flash(f"Added {name} with box ({row_digit}, {col_digit}).")
            except mysql.connector.IntegrityError:
                mydb.rollback()
                flash(f"Box ({row_digit}, {col_digit}) is already taken.", "error")
            cur.close()
        else:
            flash("Invalid input: name required, row and col must be 0–9.", "error")

    cur = mydb.cursor()
    cur.execute(
        "SELECT id, name, row_digit, col_digit, total_points, games_won FROM box_pool_participants ORDER BY total_points DESC, games_won DESC"
    )
    participants = cur.fetchall()
    mydb.close()

    current_round = get_current_round()
    return render_template(
        "ncaa_box_pool.html",
        participants=participants,
        current_round=current_round,
    )


@app.route('/test', methods=['GET'])
def index_test():
    ## Display the HTML form template
    return render_template('hello_world.html')

# `read-form` endpoint
@app.route('/read-form', methods=['POST'])
def read_form():

    # Get the form data as Python ImmutableDict datatype
    data = request.form

    ## Return the extracted information
    return {data}


if __name__ == '__main__':
    app.run()
