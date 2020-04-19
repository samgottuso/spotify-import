echo creating new sqllite database
touch spotipy.db
sqlite3 spotipy.db "CREATE TABLE missing_tracks(id INTEGER PRIMARY KEY AUTOINCREMENT,song VARCHAR(50),artist VARCHAR(50),album VARCHAR(50),year INTEGER,type VARCHAR(50));"
