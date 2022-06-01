from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class SrealityScraper():

  def __init__(self, reality_aggregator=None):

    self.reality_aggregator = reality_aggregator
    self.main_url = self.reality_aggregator.config.sreality

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
        self.reality_aggregator.existing_links.append(link_url)

    print(f'Found {len(self.reality_aggregator.reality_links)} apartments')


