import json 

class OutputCleaner():

    def cleanDuplicates(self, json_input):
        # Remove duplicate listings if any 
        unique_json = { each['id']:  each for each in json_input }.values()

        return unique_json
    

if __name__ == '__main__':
    file_name = 'scrape-output/prodaja-stanovazagreb.json'

    with open(file_name) as f:
        original = json.load(f)

    a = OutputCleaner()
    test = a.cleanDuplicates(file_name)