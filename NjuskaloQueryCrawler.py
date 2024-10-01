from bs4 import BeautifulSoup
import json
import time
import os
import random
import re

class NjuskaloQueryCrawler():
    #The blacklisted links which should be skipped
    blacklistedLinks = {'/luksuzne-nekretnine'}

    #Gets a list of all possible entities on the page. An entity is an entry to the njuskalo website.
    def _getPossibleEntities(self, soup):
        regularEntityList = soup.find('div', class_='EntityList--ListItemRegularAd')
        vauVauEntityList = soup.find('div', class_='EntityList--VauVau')
        entities = []
        if (regularEntityList != None):
            entities = regularEntityList.find_all('li', class_='EntityList-item')
        if (vauVauEntityList != None):
            entities.extend(vauVauEntityList.find_all('li', class_='EntityList-item'))
        return entities
    
    #Inserts a possible entity into parsed items which will be exported to the json
    def _crawlEntity(self, parsed_items, entity):
        if (entity.find('article', class_='entity-body') == None):
            return
        
        #Prep of entity description for easier parsing
        description_str_raw = entity.find('div', class_='entity-description-main').text
        living_area_str = re.search(r'(\d+(\.\d+)?)\s* m2', description_str_raw)
        location_str = re.search(r'Lokacija:\s*(.*)', description_str_raw)

        name_data = entity.find('a')

        name_str = name_data.text
        link_str = name_data['href']
        # location_str = entity.find('div', class_='entity-description-main').text
        published_str = entity.find('time').text
        price_str = entity.find('strong', class_='price--hrk').text

        print("Scraped " + name_str)

        parsed_items.append({
                            'name' : name_str.strip(),
                            'location' : location_str.group(1),
                            'Living Area': living_area_str.group(0),
                            'price' : price_str.strip(),
                            'link' : link_str,
                            'published' : published_str,
                    })
    
    #Write a category into a file on disk
    def _crawlCategoryLink(self, category_href, page, out_folder, page_limit):
        page.goto('https://www.njuskalo.hr' + category_href)

        currentPage = 1
        parsed_items_from_category = []
        charsToRemoveFromFilename='/?'
        charsToRemoveFromFilenameRegex = f'[{re.escape(charsToRemoveFromFilename)}]'
        
        while (True):
            html_from_page = page.content()
            soup = BeautifulSoup(html_from_page, 'html.parser')
            entities = self._getPossibleEntities(soup)

            self.out_file_path = os.path.join(out_folder, re.sub(charsToRemoveFromFilenameRegex, '', category_href) + '.json')
            
            file = open(self.out_file_path, 'w', encoding='utf-8')
                
            for entity in entities:
                self._crawlEntity(parsed_items_from_category, entity)

            parsed_items_string_json = json.dumps(parsed_items_from_category, ensure_ascii=False, indent=2)
            file.write(parsed_items_string_json)

            print('Parsed page: '+ str(currentPage))


            currentPage = currentPage + 1
            nextPageLink = self._getNextPageLink(soup)
            shouldConsiderPageLimit = page_limit != None
            if ((nextPageLink == None) or (shouldConsiderPageLimit and (page_limit == (currentPage - 1)))):
                file.close()
                break
            else:
                #sleep to give it a bit of human behavior
                time.sleep(random.uniform(0.05, 0.25))

                page.goto(nextPageLink)

    #The crawling mechanism for user picked categories:
    def crawlSelectedCategory(self, page, options):
        page.goto('https://www.njuskalo.hr')

        time.sleep(random.uniform(3,4.5))

        self._crawlCategoryLink(options.categoryHref, page, options.outFolder, options.pageLimit)

    #DeepDive crawl for real-estate - extracts location data
    def _getListingDetail(self, listing_page, listing_json):

        html_from_page = listing_page.content()
        listing = BeautifulSoup(html_from_page, 'html.parser')

        # Find lat/long string in html source
        map_regex = r'"center":\[(\d+\.\d+),(\d+\.\d+)\].*?"lat":(\d+\.\d+),"lng":(\d+\.\d+),"approximate":(true|false)'
        coordinates_matches = re.search(map_regex, html_from_page)

        if coordinates_matches:
            listing_json['coords'] = [float(coordinates_matches[1]), float(coordinates_matches[2])] # [lng, lat]
            listing_json['approx_location'] = coordinates_matches[5]
        else: 
            listing_json['coords'] = [None, None]
            listing_json['approx_location'] = None


        publisher_data = listing.find('h3', class_='ClassifiedDetailOwnerDetails-title')
        
        if publisher_data:
            listing_json['publisher'] = [publisher_data.a.text, publisher_data.a['href']]
        else:
            listing_json['publisher'] = 'Error'

        
    def listingsDetailCrawl(self, page, input_file, json_data):

        page.goto('https://www.njuskalo.hr')
        time.sleep(random.uniform(3,4.5))

        # with open(input_file, 'r') as data_file:
        #     listings_json = json.load(data_file)
        totalListingCount = len(json_data)

        for ii, listings in enumerate(json_data):

            print(f"Scraping {ii} out of {totalListingCount}")
            
            address = 'https://www.njuskalo.hr' + listings['link'] # access page
            
            
            page.goto(address, timeout=150000)
            time.sleep(random.uniform(3,4.5))

            listings = self._getListingDetail(page, listings)

            # Write to file
            with open(input_file, 'w') as data_file:
                parsed_items_string_json = json.dumps(json_data, ensure_ascii=False, indent=2)
                data_file.write(parsed_items_string_json)
    
    #If there is no page after this, returns None
    def _getNextPageLink(self, soup):
        try:
            pagination_html = soup.find('ul', class_='Pagination-items')
            nextButtonSpan = pagination_html.find('span', text='»')
            if (nextButtonSpan == None):
                return None
            else:
                try:
                    return nextButtonSpan.parent['data-href']
                except:
                    return nextButtonSpan.parent['href']
        except:
            return None
        
