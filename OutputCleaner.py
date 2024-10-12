import json 
import sqlite3

class OutputCleaner():

    def __init__(self):
        self.con = sqlite3.connect("scrape-output/test.db")
        self.cur = self.con.cursor()

    def _setupTable (self): 
        self.cur.execute("CREATE TABLE movie(title, year, score)")

    def cleanDuplicates(self, json_input):
        # Remove duplicate listings if any 
        unique_json = { each['id']:  each for each in json_input }.values()

        return unique_json
    

if __name__ == '__main__':
    file_name = 'scrape-output/prodaja-stanovazagreb.json'

    # with open(file_name) as f:
    #     original = json.load(f)

    a = OutputCleaner()
    # test = a.cleanDuplicates(file_name)
    # a._setupTable()
    res = a.cur.execute("SELECT name FROM sqlite_master")
    print( res.fetchone())
    # print ("hello world")