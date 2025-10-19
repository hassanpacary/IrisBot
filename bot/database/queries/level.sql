-- name: create_table_levels
CREATE TABLE IF NOT EXISTS levels (
    user INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0,
    next_level INTEGER DEFAULT 50
                                  );

-- name: insert_user
INSERT INTO levels (user)
VALUES (?);

-- name: fetch_all
SELECT user,
       xp,
       level,
       next_level
FROM levels
WHERE user = ?;

-- name: update_xp
UPDATE levels
SET xp = ?
WHERE user = ?;

-- name: update_level
UPDATE levels
SET level = ?,
    next_level = ?
WHERE user = ?

-- name: fetch_leaderboard
SELECT user,
xp,
level,
next_level
FROM levels
ORDER BY level DESC, xp DESC