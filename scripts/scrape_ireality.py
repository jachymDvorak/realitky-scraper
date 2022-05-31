from bs4 import BeautifulSoup
import requests

class IrealityScraper():

    def __init__(self, reality_aggregator=None):

        self.main_url = 'https://reality.idnes.cz/s/pronajem/byty/nad-18000-do-25000-za-mesic/?s-l=VUSC-19%3BMOP-35%3BMOP-27%3BMOP-86%3BMOP-108&s-qc%5BsubtypeFlat%5D%5B0%5D=21&s-qc%5BsubtypeFlat%5D%5B1%5D=3k&s-qc%5BsubtypeFlat%5D%5B2%5D=31&s-qc%5Blocality%5D%5B0%5D=VUSC-19&s-qc%5Blocality%5D%5B1%5D=MOP-35&s-qc%5Blocality%5D%5B2%5D=MOP-27&s-qc%5Blocality%5D%5B3%5D=MOP-86&s-qc%5Blocality%5D%5B4%5D=MOP-108'
        self.reality_aggregator = reality_aggregator

    def scrape(self):

        soup = BeautifulSoup(requests.get(self.main_url).content, 'lxml')
        ap_list_elem = soup.select('a.c-products__link')

        for link in ap_list_elem:
            link_url = link.get("href")
            if link_url in self.reality_aggregator.existing_links:
                print(f'Link {link_url} exists!')
            else:
                self.reality_aggregator.append_to_txt(link_url)
                self.reality_aggregator.reality_links.append(link_url)

        self.reality_aggregator.reality_links = list(dict.fromkeys(self.reality_aggregator.reality_links))  # Remove duplicates
        print(f'Found {len(self.reality_aggregator.reality_links)} apartments')
