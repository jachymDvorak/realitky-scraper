from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

from scripts.utils.utils import append_to_txt

import os

MAIN_URL = "https://www.sreality.cz/hledani/pronajem/byty/praha-2,praha-3,praha-6,praha-7,praha-8,praha-10?velikost=3%2B1,3%2Bkk,2%2B1&plocha-od=60&plocha-do=100&cena-od=18000&cena-do=25000"

options = Options()
options.add_argument('headless')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--remote-debugging-port=9222')

def sreality_scrape(MAIN_URL = MAIN_URL):
  print('Running webdriver...')
  i = 1
  driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
  url = f'{MAIN_URL}strana={i}'  # Otevri URL hledani bytu
  driver.get(url)  # otevri v chromu url link
  time.sleep(6)
  page_soup = BeautifulSoup(driver.page_source, 'lxml')  # page_soup pro beautifulsoup nacte html otevrene stanky
  driver.quit()
  title_elem = page_soup.select('a.title')

  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, 'links.txt')
  with open(filename, 'r') as f:
    existing_links = f.readlines()
    existing_links = [line.rstrip() for line in existing_links]

  apart_links = []
  for link in title_elem:  # projdi kazdy a.title
    link_url = 'https://sreality.cz' + link.get('href')
    if link_url in existing_links:
      print(f'Link {link_url} exists!')
    else:
      append_to_txt(link_url, filename)
      apart_links.append(link_url)  # uloz odkaz na inzerat

  apart_links = list(dict.fromkeys(apart_links))  # odstan duplicity
  print(f'Found {len(apart_links)} apartments')
  ### setup
  return apart_links

