import schedule
import time

from scripts.scrape_sreality import sreality_scrape
from scripts.email_sender import send_email


new_apts = sreality_scrape()

# if new_apts:
#     send_email(receiver_email="jachymdv@gmail.com", links=new_apts)
#     send_email(receiver_email="viktorie.havlickova@gmail.com", links=new_apts)
#
# else:
#     print('No new appartments found')

def run_scraper_send_email():

    new_apts = sreality_scrape()

    if new_apts:
        send_email(receiver_email="jachymdv@gmail.com", links=new_apts)
        send_email(receiver_email="viktorie.havlickova@gmail.com", links=new_apts)
    else:
        print('No new appartments found')

schedule.every(15).minutes.do(run_scraper_send_email)

while True:
    schedule.run_pending()
    time.sleep(1)

