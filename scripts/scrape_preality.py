from bs4 import BeautifulSoup
import requests
from scripts.utils.utils import append_to_txt
import os

def preality_scrape(URL_BASE = 'https://www.prazskereality.cz'):

  MAIN_URL = f'{URL_BASE}/pronajem-bytu?ruian=MP27,MP35,MP86,MP108&advert_subtype=_2_1,_3_1,_3_KT&advert_price=17000,25000'

  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, 'links.txt')
  print(filename)
  with open(filename, 'r') as f:
    existing_links = f.readlines()
    existing_links = [line.rstrip() for line in existing_links]

  soup = BeautifulSoup(requests.get(MAIN_URL).content, 'html.parser')

  apart_links = []
  while True:
    for apart in soup.select('div.results-list-item'):
      link_url = apart.find("a").attrs.get("href")
      link_url = f'{URL_BASE}{link_url}'
      apart_links.append(link_url)
    next_btn = soup.select_one('a.btn-next')
    if not next_btn:
      break
    next_page_lnk = URL_BASE + next_btn.attrs.get('href')
    soup = BeautifulSoup(requests.get(next_page_lnk).content, 'html.parser')

  aparts = []
  for link in apart_links:
    if link in existing_links:
      print(f'Link {link} exists!')

    else:
      append_to_txt(link, filename)
      aparts.append(link)


  print(f'Found {len(aparts)} apartments')

  return aparts
