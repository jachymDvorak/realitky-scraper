from bs4 import BeautifulSoup
import requests
from scripts.reality_aggregator import RealityAggregator

class IrealityScraper():

    def __init__(self,
                 reality_aggregator: RealityAggregator):

        self.reality_aggregator = reality_aggregator
        # get main url from config
        self.main_url = self.reality_aggregator.config.ireality

    def scrape(self) -> None:

        try:

            print(f'Scraping ireality from url: {self.main_url}')
            # create soup object of html of main url
            soup = BeautifulSoup(requests.get(self.main_url).content, 'lxml')
            # get all links of apts
            ap_list_elem = soup.select('a.c-products__link')

            i = 0
            # for each link, get the url from href
            for link in ap_list_elem:
                link_url = link.get("href")

                # if the link exists in the database, ignore
                if link_url in self.reality_aggregator.existing_links:
                    print(f'Link {link_url} exists!')

                # else: 1. add to database; 2. append to new apts list; 3. append to existing links list
                else:
                    self.reality_aggregator.append_to_txt(link_url)
                    self.reality_aggregator.reality_links.append(link_url)
                    self.reality_aggregator.existing_links.append(link_url)
                    i += 1

            # print number of new found apts
            print(f'Found {i} apartments')

        except:
            print('URL not provided.')