
from NjuskaloCrawler import NjuskaloCrawler
from CrawlingOptions import CustomCategoryCrawlingOptions
from NjuskaloTab import NjuskaloTab
from enum import Enum

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

class TerminalEngine:

    def __init__(self):
        self.category_href = ''
        self.page_num_option = None
        self.data_folder = ''
        self.out_file = ''
    
    def _runCustomCategory(self):
        print("Pick a category link to crawl: '/prodaja-kuca', '/prodaja-kuca/istra', etc...")
        print("This is basically everyhing after www.njuskalo.hr in the link in chrome")

        self.category_href = input()

        print("Do you want a limit on the pages scraped? If you do enter the amount of pages, if not enter 0 or something which isn't a digit")

        choice = input()

        if (choice != '0' and choice.isdigit()):
            self.page_num_option = int(choice)
        
        print("Enter the directory to save - input should be relative path!")

        self.data_folder = input()

        options = CustomCategoryCrawlingOptions(self.category_href, self.data_folder, self.page_num_option)
        self.crawler = NjuskaloCrawler()
        self.crawler.crawlCustomCategory(options = options)

    def _runDeepScan(self, self_run_flag = False):

        match self_run_flag:
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
                    self.crawler.listingDeepDive()
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
            self._runDeepScan(True)
            print ('Hope you like this tool! Please leave a star on github if you did :)! \n\n')