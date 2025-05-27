import sqlite3
import json

class AutoComplete:
    def __init__(self):
        self.conn = sqlite3.connect("autocompleteDB.sqlite3", autocommit=True)
        cur = self.conn.cursor()
        res = cur.execute("SELECT name FROM sqlite_master WHERE name='WordMap'")
        tables_exist = res.fetchone()

        if not tables_exist:
            self.conn.execute("CREATE TABLE WordMap(name TEXT, value TEXT)")
            self.conn.execute('CREATE TABLE WordPrediction (name TEXT, value TEXT)')
            cur.execute("INSERT INTO WordMap VALUES (?, ?)", ("wordsmap", "{}",))
            cur.execute("INSERT INTO WordPrediction VALUES (?, ?)", ("predictions", "{}",))

    def train(self, sentence):
        cur = self.conn.cursor()
        word_list = sentence.split(" ")

        words_map = cur.execute("SELECT value FROM WordMap WHERE name='wordsmap'").fetchone()[0]
        words_map = json.loads(words_map)

        predictions = cur.execute("SELECT value FROM WordPrediction WHERE name='predictions'").fetchone()[0]
        predictions = json.loads(predictions)

        for index in range(len(word_list)-1) :
            current_word, next_word  






