"""
Centralized NCAA tournament round detection and point schedule for box pool.
Adjust date ranges and points_per_round here for each year if needed.
"""
from datetime import datetime
from datetime import timedelta

# Points awarded per game by round (1 = First Four/R64, 6 = Championship)
POINTS_PER_ROUND = {
    1: 100,
    2: 200,
    3: 450,
    4: 750,
    5: 1000,
    6: 3000,
}

# Round name for display
ROUND_NAMES = {
    0: "First Four",
    1: "Round 1",
    2: "Round 2",
    3: "Sweet 16",
    4: "Elite 8",
    5: "Final Four",
    6: "Championship",
}

# Date ranges for round detection (EDT). Update for each tournament year.
def get_round_from_date(game_date_edt):
    """
    Return round number 1-6 based on game date (in EDT), or 0 if outside known windows.
    game_date_edt: datetime (naive, interpreted as EDT).
    """
    if game_date_edt < datetime(2026, 3, 19):
        return 0
    if game_date_edt < datetime(2025, 3, 21):
        return 1
    if game_date_edt < datetime(2026, 3, 23):
        return 2
    if game_date_edt < datetime(2026, 3, 28):
        return 3
    if game_date_edt < datetime(2026, 3, 30):
        return 4
    if game_date_edt < datetime(2026, 4, 5):
        return 5
    if game_date_edt < datetime(2026, 4, 7):
        return 6
    return 0


def get_current_round(utc_now=None):
    """
    Return current round number for display (e.g. leaderboard). Uses EDT.
    utc_now: optional datetime (default now).
    """
    if utc_now is None:
        utc_now = datetime.utcnow()
    edt = utc_now - timedelta(hours=4)
    return get_round_from_date(edt)


def get_points_for_round(round_num):
    """Return points awarded for a game in the given round (1-6). Returns 0 for round 0 or unknown."""
    return POINTS_PER_ROUND.get(round_num, 0)
