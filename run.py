#import schedule
#import time

from scripts.email_sender import send_email
from scripts.scrape_sreality import sreality_scrape
from scripts.scrape_preality import preality_scrape
from scripts.scrape_ireality import ireality_scrape
from scripts.utils.utils import join_all_scrape_results

# TODO: Class that takes in all links to get rid of the fnc below, class as arg to scrapers, add send email func to class
# TODO: async scrapers?

sreality_apts = sreality_scrape()
preality_apts = preality_scrape()
ireality_apts = ireality_scrape()

new_apts = join_all_scrape_results([sreality_apts, preality_apts, ireality_apts])

if new_apts:
    send_email(receiver_email="jachymdv@gmail.com", links=new_apts)
    send_email(receiver_email="viktorie.havlickova@gmail.com", links=new_apts)
else:
    print('No new apartments found')

# schedule.every(15).minutes.do(run_scraper_send_email)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

