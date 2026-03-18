"""
NCAA March Madness Box Pool: score calculation.
Run after fetching games. For each finished game not yet in box_pool_scored_games,
determines winning box (home_score % 10, away_score % 10), awards points to that
participant, and records the game as scored.
"""
import mysql.connector

import config
from ncaa_rounds import get_points_for_round

def run():
    params = config.get_mysql_connection_params()
    mydb = mysql.connector.connect(**params)

    # Game IDs already scored for box pool
    cur_scored = mydb.cursor()
    cur_scored.execute("SELECT game_id FROM box_pool_scored_games")
    scored_game_ids = set(row[0] for row in cur_scored.fetchall())

    # Finished games from ncaa_games that we haven't scored yet
    cur_games = mydb.cursor()
    cur_games.execute(
        "SELECT id, home_score, away_score, round FROM ncaa_games "
        "WHERE status IN ('Ended', 'AET')"
    )
    games = cur_games.fetchall()

    for (game_id, home_score, away_score, game_round) in games:
        if game_id in scored_game_ids:
            continue

        # Exclude Round 1 games from any box-pool participant stats.
        # We still mark them as "scored" to avoid reprocessing on later runs.
        if game_round == 1:
            cur_ins = mydb.cursor()
            cur_ins.execute(
                "INSERT IGNORE INTO box_pool_scored_games (game_id) VALUES (%s)",
                (game_id,),
            )
            mydb.commit()
            continue

        home_ones = int(home_score) % 10
        away_ones = int(away_score) % 10
        points = get_points_for_round(game_round)
        if points == 0:
            continue

        # Find participant with this box (row_digit = home_ones, col_digit = away_ones)
        cur_part = mydb.cursor()
        cur_part.execute(
            "SELECT id, total_points, games_won FROM box_pool_participants "
            "WHERE row_digit = %s AND col_digit = %s",
            (home_ones, away_ones)
        )
        row = cur_part.fetchone()
        if not row:
            # No participant has this box; still mark game as scored
            cur_ins = mydb.cursor()
            cur_ins.execute("INSERT IGNORE INTO box_pool_scored_games (game_id) VALUES (%s)", (game_id,))
            mydb.commit()
            continue

        part_id, total_points, games_won = row
        new_total = total_points + points
        new_won = games_won + 1

        cur_update = mydb.cursor()
        cur_update.execute(
            "UPDATE box_pool_participants SET total_points = %s, games_won = %s WHERE id = %s",
            (new_total, new_won, part_id)
        )
        cur_ins = mydb.cursor()
        cur_ins.execute("INSERT INTO box_pool_scored_games (game_id) VALUES (%s)", (game_id,))
        mydb.commit()

    mydb.close()

if __name__ == "__main__":
    run()
