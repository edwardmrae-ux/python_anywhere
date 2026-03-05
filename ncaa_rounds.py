"""
Centralized NCAA tournament round detection and point schedule for box pool.
Adjust date ranges and points_per_round here for each year if needed.
"""
from datetime import datetime
from datetime import timedelta

# Points awarded per game by round (1 = First Four/R64, 6 = Championship)
POINTS_PER_ROUND = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
}

# Round name for display
ROUND_NAMES = {
    0: "—",
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
    if game_date_edt < datetime(2025, 3, 20):
        return 0
    if game_date_edt < datetime(2025, 3, 22):
        return 1
    if game_date_edt < datetime(2025, 3, 24):
        return 2
    if game_date_edt < datetime(2025, 3, 29):
        return 3
    if game_date_edt < datetime(2025, 3, 31):
        return 4
    if game_date_edt < datetime(2025, 4, 7):
        return 5
    if game_date_edt < datetime(2025, 4, 9):
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
