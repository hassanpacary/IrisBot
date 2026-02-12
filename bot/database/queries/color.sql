-- name: create_table_colors
CREATE TABLE IF NOT EXISTS colors (
    user INTEGER PRIMARY KEY,
    color INTEGER DEFAULT 0
                                  );

-- name: insert_color
INSERT INTO colors (user, color)
VALUES (?, ?);

-- name: fetch_all
SELECT user,
       color
FROM colors
WHERE user = ?;

-- name: update_color
UPDATE colors
SET color = ?
WHERE user = ?;