import sys
import logging
import sqlite3


class Database:
    connection = None
    cursor = None

    def __init__(self, path_to_db):
        try:
            self.connection = sqlite3.connect(path_to_db)
        except sqlite3.OperationalError:
            logging.error('Cannot open database file "{}"'.format(path_to_db))
            sys.exit(-1)

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS music (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,

                PATH TEXT NOT NULL,
                TRACK_LENGTH INTEGER,

                TAG_TITLE TEXT,
                TAG_ARTIST TEXT,
                TAG_ALBUM TEXT,
                TAG_GENRE TEXT,
                TAG_TRACK INTEGER,
                TAG_YEAR INTEGER
            );
        """)

    def __del__(self):
        if self.connection:
            self.connection.close()

    def record_music_info(self, metadata_array):
        for track in metadata_array:
            meta = [(
                track.filename,
                track.info.length,
                track.tags['TITLE'][0],
                track.tags['ARTIST'][0],
                track.tags['ALBUM'][0],
                track.tags['GENRE'][0],
                track.tags['TRACKNUMBER'][0],
                track.tags['DATE'][0]
            )]

            self.cursor.executemany('INSERT INTO music VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)', meta)

        self.connection.commit()