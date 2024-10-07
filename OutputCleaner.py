import json 

class OutputCleaner():

    def cleanDuplicates(json_input):
        # Remove duplicate listings if any 
        unique_json = { each['id']:  each for each in json_input }.values()

        return unique_json