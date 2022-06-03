from scripts.reality_aggregator import RealityAggregator
from scripts.config import Config
from scripts.scrape_ireality import IrealityScraper
from scripts.scrape_preality import PrealityScraper
from scripts.scrape_sreality import SrealityScraper
from scripts.scrape_breality import BrealityScraper
import argparse

# TODO: async scrapers?

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Real estate scraper')
    parser.add_argument('-c', '--config-name', help='Name of the config file', default='config.yaml')
    arguments = parser.parse_args()

    config = Config(arguments.config_name)

    print(f'Config name: {config.config_name}')

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
        print(f'Found {len(reality_aggregator.reality_links)} new apartments!')

        if reality_aggregator.config.send_messages == 'email':
            for email in reality_aggregator.config.emails:
                print(f'Sending email to {email}...')
                reality_aggregator.send_email(receiver_email=email)
        if reality_aggregator.config.send_messages == 'telegram':
            print(f'Sending links to telegram group...')
            reality_aggregator.send_telegram_messages()

    else:
        print('No new apartments found')

    # schedule.every(15).minutes.do(run_scraper_send_email)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

