from bs4 import BeautifulSoup
import requests

class PrealityScraper():

    def __init__(self, reality_aggregator=None):

        self.url_base = 'https://www.prazskereality.cz'
        self.main_url = f'{self.url_base}/pronajem-bytu?ruian=MP27,MP35,MP86,MP108&advert_subtype=_2_1,_3_1,_3_KT&advert_price=17000,25000'
        self.reality_aggregator = reality_aggregator

    def scrape(self):

        soup = BeautifulSoup(requests.get(self.main_url).content, 'html.parser')

        while True:
            for apart in soup.select('div.results-list-item'):
                link_url = apart.find("a").attrs.get("href")
                link_url = f'{self.url_base}{link_url}'
                if link_url in self.reality_aggregator.existing_links:
                    print(f'Link {link_url} exists!')
                else:
                    self.reality_aggregator.reality_links.append(link_url)
                    self.reality_aggregator.append_to_txt(link_url)

            next_btn = soup.select_one('a.btn-next')
            if not next_btn:
                break
            next_page_lnk = URL_BASE + next_btn.attrs.get('href')
            soup = BeautifulSoup(requests.get(next_page_lnk).content, 'html.parser')

        self.reality_aggregator.reality_links = list(dict.fromkeys(self.reality_aggregator.reality_links))
        print(f'Found {len(self.reality_aggregator.reality_links)} apartments')
