from scripts.reality_aggregator import RealityAggregator
from scripts.config import Config
from scripts.scrape_ireality import IrealityScraper
from scripts.scrape_preality import PrealityScraper
from scripts.scrape_sreality import SrealityScraper
from scripts.scrape_breality import BrealityScraper
# TODO: async scrapers?

config = Config()

reality_aggregator = RealityAggregator(config)
ireality_scraper = IrealityScraper(reality_aggregator)
preality_scraper = PrealityScraper(reality_aggregator)
sreality_scraper = SrealityScraper(reality_aggregator)
breality_scraper = BrealityScraper(reality_aggregator)

ireality_scraper.scrape()
preality_scraper.scrape()
sreality_scraper.scrape()
breality_scraper.scrape()

if reality_aggregator.reality_links:
    for email in reality_aggregator.config.emails:
        print(f'Sending email to {email}...')
        reality_aggregator.send_email(receiver_email=email)
else:
    print('No new apartments found')
#
# # schedule.every(15).minutes.do(run_scraper_send_email)
# #
# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)

