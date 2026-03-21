-- NCAA March Madness Box Pool tables
-- Run against database: erae22$ncaa_tourney

-- Participants: one row per box assignment; multiple rows can share participant_id (same person, different boxes).
-- row_digit/col_digit: ones digits of home/away final score for that box.
--
-- Existing databases: add the column before relying on this file for upgrades, e.g.:
--   ALTER TABLE box_pool_participants ADD COLUMN participant_id INT NULL;
--   (backfill participant_id per row, then:)
--   ALTER TABLE box_pool_participants MODIFY participant_id INT NOT NULL;
CREATE TABLE IF NOT EXISTS box_pool_participants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    row_digit TINYINT NOT NULL,
    col_digit TINYINT NOT NULL,
    total_points INT NOT NULL DEFAULT 0,
    games_won INT NOT NULL DEFAULT 0,
    UNIQUE KEY unique_box (row_digit, col_digit)
);

-- Game IDs that have already been scored for the box pool (avoids double-counting)
CREATE TABLE IF NOT EXISTS box_pool_scored_games (
    game_id BIGINT PRIMARY KEY
);
