import sqlite3
import traceback


class Model:
    def __init__(self):
        self.song_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = sqlite3.connect("test.db")
            self.cur = self.conn.cursor()
           
        except sqlite3.DatabaseError:
            self.db_status = False
            
    def get_db_status(self):
        return self.db_status

    def get_song_count(self):
        return len(self.song_dict)

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()

        if self.conn is not None:
            self.conn.close()

    def add_song(self, song_names, song_paths):
        i=0
        for song_name in song_names:
            self.song_dict[song_name] = song_paths[i]
            i=i+1

    def get_song_path(self, song_name):
        return self.song_dict[song_name]

    def remove_song(self, song_name):
        self.song_dict.pop(song_name)

    def search_song_in_favourites(self, song_name):
        self.cur.execute(
            "select song_name from myfavourites where song_name=:1", (song_name,))
        song_tuple = self.cur.fetchone()
        if song_tuple is None:
            return False
        else:
            return True

    def add_song_to_favourites(self, song_name, song_path):
        is_song_present = self.search_song_in_favourites(song_name)
        if is_song_present == True:
            return "Song alreasdy present in favourites"
        self.cur.execute("select max(song_id) from myfavourites")
        last_song_id = self.cur.fetchone()[0]
        next_song_id = 1
        if last_song_id is not None:
            next_song_id = last_song_id+1
        self.cur.execute(
            "insert into myfavourites values(:1,:2,:3)", (next_song_id, song_name, song_path))
        self.conn.commit()
        return "Song successfully added to your favourites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from myfavourites")
        songs_present = False
        for song_name, song_path in self.cur:
            self.song_dict[song_name] = song_path
            songs_present = True
        if songs_present:
            return "List populated from favourites"
        else:
            return "No songs present i your favourites"

    def remove_song_from_favourites(self, song_name):
        self.cur.execute(
            "Delete from myfavourites where song_name=:1", (song_name,))
        count = self.cur.rowcount
        if count == 0:
            return "Song not present in your favourites"
        else:
            self.song_dict.pop(song_name)
            self.conn.commit()
            return "Song deleted from your favourites"
