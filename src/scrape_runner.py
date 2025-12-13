from scrape_data import ScrapeData
import os 
import yaml 
from scraper_output import ScraperOutput
import time


def return_config_urls() -> str:
    print(os.getcwd())
    with open('./src/urls.yaml', 'r') as config:
        loaded_config = yaml.safe_load(config)

    return loaded_config['urls']


class ScrapeRunner():


    def __init__(self):
        self.scrape_data_class = ScrapeData()
        self.urls = return_config_urls()

    
    def run_scraper(self):
        for site in self.urls:
            self.scrape_data_class.scrape_data(site)

            ai_scraper_results = self.scrape_data_class.export_ai_result_json


            scraper_output = ScraperOutput(ai_scraper_results)
            scraper_output.scraper_json_output()
            time.sleep(10) #avoid exceeding tpm/rqm of api 

