import json 
import sqlite3

class OutputStandardizer():

    def __init__(self, file_name):
        self.json_dataset = self._readJsonFile(file_name)
        self.con = sqlite3.connect("scrape-output/test.db")
        self.cur = self.con.cursor()

    def _readJsonFile(self, file_name): 
        # Reads json file with listings data and stores them as a dict object
        with open(file_name, 'r') as f:
            file_data = json.load(f)

        return file_data

    def _generateTable (self): 
        self.cur.execute("CREATE TABLE movie(title, year, score)")

    def cleanDuplicates(self):
        # Remove duplicate listings if any 
        unique_json = { each['id']:  each for each in self.json_dataset }.values()

        return unique_json
    

if __name__ == '__main__':
    file_name = 'scrape-output/prodaja-stanovazagreb.json'

    # with open(file_name) as f:
    #     original = json.load(f)

    a = OutputStandardizer(file_name)
    print(len(a.json_dataset))
    aa = a.cleanDuplicates()
    print(len(aa))

    # test = a.cleanDuplicates(file_name)
    # a._setupTable()
    # res = a.cur.execute("SELECT name FROM sqlite_master")
    # print( res.fetchone())
    # print ("hello world")