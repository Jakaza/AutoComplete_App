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
            current_word, next_word = word_list[index] , word_list[index+1]
            if current_word not in words_map :
             words_map[current_word] = {}
            if next_word not in words_map[current_word] :
             words_map[current_word][next_word] = 1
            else :
               words_map[current_word][next_word] += 1

            if current_word not in predictions:
               predictions[current_word] = {
                   'completion_word': next_word,
                   'completion_count': 1
               }
            else:
               if words_map[current_word][next_word] > predictions[current_word]['completion_count']:
                predictions[current_word]['completion_word'] = next_word
                predictions[current_word]['completion_count'] = words_map[current_word][next_word]

        
        words_map = json.dumps(words_map)
        predictions = json.dumps(predictions)

        cur.execute("UPDATE WordMap SET value = (?) WHERE name='wordsmap'", (words_map,))
        cur.execute("UPDATE WordPrediction SET value = (?) WHERE name='predictions'", (predictions,))

        return("training complete")
    
    def predict(self, word):
       cur = self.conn.cursor()

       predictions = cur.execute("SELECT value FROM WordPrediction WHERE name='predictions'").fetchone()[0]
       predictions = json.loads(predictions)
       completion_word = predictions[word.lower()]['completion_word']

       return completion_word
    

autoComplete = AutoComplete()

autoComplete.train("Good morning! I hope you slept well.")
autoComplete.train("Good afternoon! How has your day been so far?")
autoComplete.train("Good night! Sweet dreams and sleep tight.")
autoComplete.train("How are you?")
autoComplete.train("I’m fine, thank you.")
autoComplete.train("What is your name?")
autoComplete.train("It’s nice to meet you. Let’s be friends!")

autoComplete.train("This is my bedroom where I sleep and play.")
autoComplete.train("I love my family because they take care of me.")
autoComplete.train("Please sit down.")
autoComplete.train("Can you please close the door gently?")
autoComplete.train("Let’s open the window and get some fresh air.")
autoComplete.train("I’m very hungry. Can I eat something, please?")
autoComplete.train("Close the door.")

print(autoComplete.predict("family"))







