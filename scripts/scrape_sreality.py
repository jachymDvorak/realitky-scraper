from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

import os

MAIN_URL = "https://www.sreality.cz/hledani/pronajem/byty/praha-2,praha-3,praha-6,praha-7,praha-8,praha-10?velikost=3%2B1,3%2Bkk,2%2B1&plocha-od=60&plocha-do=100&cena-od=18000&cena-do=30000"

options = Options()
options.add_argument('headless')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--remote-debugging-port=9222')

def sreality_scrape(debug=False, MAIN_URL = MAIN_URL):
  print('Running webdriver...')
  # Ziskani pocet stranek
  propertyLinks = []
  i = 1

  print(f'Scraping page: {i}')
  driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
  prefix = DEBUG_URL if debug else MAIN_URL
  url = f'{prefix}strana={i}'  # Otevri URL hledani bytu
  driver.get(url)  # otevri v chromu url link
  time.sleep(6)
  page_soup = BeautifulSoup(driver.page_source, 'lxml')  # page_soup pro beautifulsoup nacte html otevrene stanky
  driver.quit()
  title_elem = page_soup.select('a.title')

  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, 'links.txt')
  print(filename)
  with open(filename, 'r') as f:
    existing_links = f.readlines()
    existing_links = [line.rstrip() for line in existing_links]

  for link in title_elem:  # projdi kazdy a.title
    link_url = 'https://sreality.cz' + link.get('href')
    if link_url in existing_links:
      print(f'Link {link_url} exists!')
    else:
      append_to_txt(link_url, filename)
      propertyLinks.append(link_url)  # uloz odkaz na inzerat

  propertyLinks = list(dict.fromkeys(propertyLinks))  # odstan duplicity
  print(f'Found {len(propertyLinks)} apartments in {i} pages')
  ### setup
  return propertyLinks


def append_to_txt(link, filename):

  print(f'Appending link to {filename}')
  with open(filename, 'a') as f:
    f.write(link)
    f.write('\n')
