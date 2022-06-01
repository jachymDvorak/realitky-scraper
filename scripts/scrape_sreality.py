from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class SrealityScraper():

  def __init__(self, reality_aggregator=None):

    self.main_url = "https://www.sreality.cz/hledani/pronajem/byty/praha-2,praha-3,praha-6,praha-7,praha-8,praha-10?velikost=3%2B1,3%2Bkk,2%2B1&plocha-od=60&plocha-do=100&cena-od=18000&cena-do=25000"
    self.reality_aggregator = reality_aggregator

  def scrape(self):

    options = Options()
    options.add_argument('headless')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')

    print('Running webdriver...')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(self.main_url)  # otevri v chromu url link
    time.sleep(6)
    page_soup = BeautifulSoup(driver.page_source, 'lxml')  # page_soup pro beautifulsoup nacte html otevrene stanky
    driver.quit()
    title_elem = page_soup.select('a.title')

    for link in title_elem:  # projdi kazdy a.title
      link_url = 'https://sreality.cz' + link.get('href')
      if link_url in self.reality_aggregator.existing_links:
        print(f'Link {link_url} exists!')
      else:
        self.reality_aggregator.reality_links.append(link_url)
        self.reality_aggregator.append_to_txt(link_url)

    self.reality_aggregator.reality_links = list(dict.fromkeys(self.reality_aggregator.reality_links))  # odstan duplicity
    print(f'Found {len(self.reality_aggregator.reality_links)} apartments')


