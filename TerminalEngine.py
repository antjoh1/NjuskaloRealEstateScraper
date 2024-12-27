
from NjuskaloCrawler import NjuskaloCrawler
from CrawlingOptions import CustomCategoryCrawlingOptions
from NjuskaloTab import NjuskaloTab
from enum import Enum
import json
import geojson
import os 

splash_message = """
****************************************************
*                                                  *
*           Welcome to Njuškalo Crawler!           *
*                                                  *
* This tool allows you to scrape and analyze data  *
* from the popular Croatian classifieds website    *
* Njuškalo. Whether you're looking for the best    *
* real estate deals, the latest tech gadgets, or   *
* just curious about market trends, this crawler   *
* has you covered.                                 *
*                                                  *
* Please ensure you have the necessary permissions *
* to scrape data and respect the website's         *
* terms of service.                                *
*                                                  *
* Happy Crawling!                                  *
*                                                  *
***************************************************

"""

class TerminalEngine():

    def __init__(self, ):
        self.category_href = ''
        self.page_lim = None
        self.data_folder = ''
        self.out_file = ''
    
    def _runCustomCategory(self):
        print("Pick a category link to crawl: '/prodaja-kuca', '/prodaja-kuca/istra', etc...")
        print("This is basically everyhing after www.njuskalo.hr in the link in chrome")

        self.category_href = input()

        print("Do you want to limit the pages scraped? If not enter 0 or any non-digit value")

        choice = input()

        if (choice != '0' and choice.isdigit()):
            self.page_lim = int(choice)
        
        print("Enter output directory - input should be given as relative path!")

        self.data_folder = input()

        options = CustomCategoryCrawlingOptions(self.category_href, self.data_folder, self.page_lim)
        self.crawler = NjuskaloCrawler()
        self.crawler.crawlCustomCategory(options = options)

    def _runDeepScan(self, run_only_deep_scan_flag = False):

        match run_only_deep_scan_flag:
            case True: 
                print ('Provide a relative path to scrape results file (.json)')

                file_choice = input()

                if file_choice != None:
                    self.crawler = NjuskaloCrawler()
                    self.crawler.listingDeepDive(file_choice)

            case _:
                print ("""Would you like to run a deep-dive scan of all listings? This will take a while but will add listing data needed for other display elements \n
                    Type '1' to run and anything else to quit. """)
                
                choice = input()

                if choice == '1':
                    target_file = self.data_folder + '/' + self.category_href.replace('/', '') + '.json'
                    self.crawler.listingDeepDive(target_file)
                    # self.convertFileToGeoJson(file_choice)
                else:
                    pass

    def runCoreLoop(self):
        print(splash_message)

        print ('(1) I want to conduct a new scrape \n (2) I want to do a deepScan of an existing scrape \n')
        choice = input()

        if choice == '1':
            self._runCustomCategory()
            print ('Crawling complete! \n')
        
            self._runDeepScan()
            print ('Hope you like this tool! Please leave a star on github if you did :)! \n\n')

        elif choice == '2':
            self._runDeepScan(run_only_deep_scan_flag=True)
            print ('Hope you like this tool! Please leave a star on github if you did :)! \n\n')


    def convertFileToGeoJson(self, target_json_file):
        """ Convert scraped json file to geojson dict """

        new_target_file = target_json_file[:-5] + ".geojson"
        features = []  # initialize feature list

        with open(target_json_file, 'r') as f:
            file_data = json.load(f)

        for data_entry in file_data:
            coord_data = data_entry.pop('coords')
            
            if None in coord_data:
                coord_data = [13.6914, 44.327395] ## This is a random placeholder coordinate in the adriatic. Need to think of a better method for blanks coords

            features.append(geojson.Feature(geometry = geojson.Point(coord_data), properties = data_entry))

        with open(new_target_file, 'w') as data_file:
            feature_collection_geojson = geojson.dumps(geojson.FeatureCollection(features))
            data_file.write(feature_collection_geojson)

if __name__  == '__main__':
    file_name = 'scrape-output/prodaja-stanovazagreb.json'
    aa = TerminalEngine()

    aa.convertFileToGeoJson(file_name)