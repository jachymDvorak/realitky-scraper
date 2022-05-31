#import schedule
#import time

#from scripts.email_sender import send_email
from scripts.reality_aggregator import RealityAggregator
from scripts.scrape_ireality import IrealityScraper
from scripts.scrape_preality import PrealityScraper
from scripts.scrape_sreality import SrealityScraper
# from scripts.scrape_sreality import sreality_scrape
# from scripts.scrape_preality import preality_scrape
# from scripts.scrape_ireality import ireality_scrape
# from scripts.utils.utils import join_all_scrape_results

# TODO: async scrapers?

reality_aggregator = RealityAggregator()
ireality_scraper = IrealityScraper(reality_aggregator)
preality_scraper = PrealityScraper(reality_aggregator)
sreality_scraper = SrealityScraper(reality_aggregator)

ireality_scraper.scrape()
preality_scraper.scrape()
sreality_scraper.scrape()

print(reality_aggregator.reality_links)

# sreality_apts = sreality_scrape()
# preality_apts = preality_scrape()
# ireality_apts = ireality_scrape()
#
# #new_apts = join_all_scrape_results([sreality_apts, preality_apts, ireality_apts])
#
if reality_aggregator.reality_links:
    print('Sending emails...')
    reality_aggregator.send_email(receiver_email="jachymdv@gmail.com")
    #send_email(receiver_email="viktorie.havlickova@gmail.com", links=new_apts)
else:
    print('No new apartments found')
#
# # schedule.every(15).minutes.do(run_scraper_send_email)
# #
# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)

