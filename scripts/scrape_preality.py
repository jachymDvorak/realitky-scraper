from bs4 import BeautifulSoup
import requests
from scripts.reality_aggregator import RealityAggregator


class PrealityScraper():

    def __init__(self,
                 reality_aggregator: RealityAggregator):

        self.url_base = 'https://www.prazskereality.cz'
        self.reality_aggregator = reality_aggregator
        self.main_url = self.reality_aggregator.config.preality

    def scrape(self) -> None:

        try:
            print(f'Scraping preality from url: {self.main_url}')
            # create soup object of html of main url
            soup = BeautifulSoup(requests.get(self.main_url).content, 'html.parser')

            i = 0

            while True:

                # for each link, get the url from href and create main url
                for apart in soup.select('div.results-list-item'):
                    link_url = apart.find("a").attrs.get("href")
                    link_url = f'{self.url_base}{link_url}'

                    # if the link exists in the database, ignore
                    if link_url in self.reality_aggregator.existing_links:
                        print(f'Link {link_url} exists!')

                    # else: 1. add to database; 2. append to new apts list; 3. append to existing links list
                    else:
                        self.reality_aggregator.reality_links.append(link_url)
                        self.reality_aggregator.append_to_txt(link_url)
                        self.reality_aggregator.existing_links.append(link_url)
                        i += 1

                # get button for next page, and scrape again, until there are no pages left
                next_btn = soup.select_one('a.btn-next')
                if not next_btn:
                    break

                # use next page link as main url
                next_page_lnk = self.url_base + next_btn.attrs.get('href')
                soup = BeautifulSoup(requests.get(next_page_lnk).content, 'html.parser')

            # print number of new found apts
            print(f'Found {i} apartments')

        except:
            print('URL not provided.')
