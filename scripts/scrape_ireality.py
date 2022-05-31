from bs4 import BeautifulSoup
import requests
import os

from scripts.utils.utils import append_to_txt

MAIN_URL = 'https://reality.idnes.cz/s/pronajem/byty/nad-18000-do-25000-za-mesic/?s-l=VUSC-19%3BMOP-35%3BMOP-27%3BMOP-86%3BMOP-108&s-qc%5BsubtypeFlat%5D%5B0%5D=21&s-qc%5BsubtypeFlat%5D%5B1%5D=3k&s-qc%5BsubtypeFlat%5D%5B2%5D=31&s-qc%5Blocality%5D%5B0%5D=VUSC-19&s-qc%5Blocality%5D%5B1%5D=MOP-35&s-qc%5Blocality%5D%5B2%5D=MOP-27&s-qc%5Blocality%5D%5B3%5D=MOP-86&s-qc%5Blocality%5D%5B4%5D=MOP-108'

def ireality_scrape(MAIN_URL = MAIN_URL):
    url = MAIN_URL

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'links.txt')
    with open(filename, 'r') as f:
        existing_links = f.readlines()
        existing_links = [line.rstrip() for line in existing_links]

    apart_links = []

    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    ap_list_elem = soup.select('a.c-products__link')

    for link in ap_list_elem:
        link_url = link.get("href")
        if link_url in existing_links:
            print(f'Link {link_url} exists!')
        else:
            append_to_txt(link_url, filename)
            apart_links.append(link_url)  # uloz odkaz na inzerat

    apart_links = list(dict.fromkeys(apart_links))  # Remove duplicates
    print(f'Found {len(apart_links)} apartments')

    return apart_links
