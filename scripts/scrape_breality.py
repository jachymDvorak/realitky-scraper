import requests
from bs4 import BeautifulSoup

class BrealityScraper():

    def __init__(self, reality_aggregator=None):

        self.url_base = 'https://www.bezrealitky.cz'
        self.reality_aggregator = reality_aggregator
        self.main_url = self.reality_aggregator.config.breality

    def scrape(self):

        soup = BeautifulSoup(requests.get(self.main_url).content, 'lxml')
        ap_list_elem = soup.find_all('a')
        for link in ap_list_elem:
            link_url = link.get("href")
            if 'nemovitosti-byty-domy' in link_url:
                if link_url in self.reality_aggregator.existing_links:
                    print(f'Link {link_url} exists!')
                else:
                    self.reality_aggregator.reality_links.append(link_url)
                    self.reality_aggregator.append_to_txt(link_url)
                    self.reality_aggregator.existing_links.append(link_url)

        print(f'Found {len(self.reality_aggregator.reality_links)} apartments')
