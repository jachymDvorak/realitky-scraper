import requests
from bs4 import BeautifulSoup
from scripts.reality_aggregator import RealityAggregator

class BrealityScraper():

    def __init__(self,
                 reality_aggregator: RealityAggregator):

        self.url_base = 'https://www.bezrealitky.cz'
        self.reality_aggregator = reality_aggregator
        self.main_urls = self.reality_aggregator.config.breality

    def scrape(self, main_url: str) -> None:

        print(f'Scraping breality from url: {main_url}')

        try:
            # create soup object of html of main url
            soup = BeautifulSoup(requests.get(main_url).content, 'lxml')
            # get all links of apts
            ap_list_elem = soup.find_all('a')

            i = 0

            # for each link, get the url from href
            for link in ap_list_elem:
                link_url = link.get("href")
                if 'nemovitosti-byty-domy' in link_url:

                    # if the link exists in the database, ignore
                    if link_url in self.reality_aggregator.existing_links:
                        print(f'Link {link_url} exists!')

                    # else: 1. add to database; 2. append to new apts list; 3. append to existing links list
                    else:
                        self.reality_aggregator.reality_links.append(link_url)
                        self.reality_aggregator.append_to_txt(link_url)
                        self.reality_aggregator.existing_links.append(link_url)
                        i += 1

            # print number of new found apts
            print(f'Found {i} apartments')

        except:
            print('URL not provided.')

    def scrape_all_urls(self):

        for url in self.main_urls:

            try:
                self.scrape(url)
            except:

                print('oops')
