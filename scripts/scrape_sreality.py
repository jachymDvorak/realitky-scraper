from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from scripts.reality_aggregator import RealityAggregator

class SrealityScraper():

  def __init__(self,
               reality_aggregator: RealityAggregator):

    self.reality_aggregator = reality_aggregator
    self.main_url = self.reality_aggregator.config.sreality

  def scrape(self) -> None:

    try:
      # options for the web driver
      options = Options()
      options.add_argument('headless')
      options.add_argument('--disable-infobars')
      options.add_argument('--disable-dev-shm-usage')
      options.add_argument('--no-sandbox')
      options.add_argument('--remote-debugging-port=9222')

      print('Running webdriver...')

      # instantiate webdriver; install webdriver according to current chrome version
      driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
      print(f'Scraping sreality from url: {self.main_url}')

      # open main url in chrome
      driver.get(self.main_url)
      time.sleep(6)

      # get html from the page
      page_soup = BeautifulSoup(driver.page_source, 'lxml')

      # quit the driver
      driver.quit()

      # select all links with apts
      title_elem = page_soup.select('a.title')

      i = 0
      # for each apt link get href
      for link in title_elem:
        link_url = 'https://sreality.cz' + link.get('href')

        # if the link exists in the database, ignore
        if link_url in self.reality_aggregator.existing_links:
          print(f'Link {link_url} exists!')

        # else: 1. add to database; 2. append to new apts list; 3. append to existing links list
        else:
          self.reality_aggregator.reality_links.append(link_url)
          self.reality_aggregator.append_to_txt(link_url)
          self.reality_aggregator.existing_links.append(link_url)
          i += 1

      # print number of new found apts
      print(f'Found {i} apartments')
    except:
      print('URL not provided.')

