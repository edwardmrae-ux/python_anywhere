# NCAA March Madness Box Pool

## Setup

1. **Create the box pool tables** in MySQL (database `erae22$ncaa_tourney`). Run the SQL in `schema_box_pool.sql` via Python Anywhere’s MySQL console or:

   ```bash
   mysql -h erae22.mysql.pythonanywhere-services.com -u erae22 -p erae22\$ncaa_tourney < schema_box_pool.sql
   ```
   (Or run the contents of `schema_box_pool.sql` in the Python Anywhere MySQL tab.)

2. **Config**: DB and RapidAPI settings are in `config.py`. For production, set env vars (e.g. on Python Anywhere): `NCAA_DB_HOST`, `NCAA_DB_USER`, `NCAA_DB_PASSWORD`, `NCAA_DB_NAME`, `RAPIDAPI_KEY`, `RAPIDAPI_HOST`, `RAPIDAPI_BASE_URL`.

## Round mapping

Round detection and points per round are centralized in **`ncaa_rounds.py`**:

- `get_round_from_date(game_date_edt)` – round 1–6 from game date (EDT).
- `get_current_round()` – current round for the UI.
- `get_points_for_round(round_num)` – points for a game in that round (1–6 pts).
- `POINTS_PER_ROUND`, `ROUND_NAMES` – adjust dates and point values here for each tournament year.

## Scheduling (Python Anywhere)

1. **Fetch games + box pool scoring**: Schedule `ncaa-pool_get_games_new.py` (e.g. every 5–10 minutes during the tournament). It fetches from RapidAPI, updates `ncaa_games` and bracket pool data, then calls the box pool score updater.
2. **Optional**: To run only box pool scoring (e.g. after manual DB updates), run: `python ncaa_box_pool_scores.py`.

## Routes

- **`/ncaa-box-pool`** – Box pool leaderboard and “Add participant” form (name, row 0–9, col 0–9).
