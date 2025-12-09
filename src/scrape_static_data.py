from fetch_html import FetchHtml
from  parse_html import ParseHTML
from scraper_output import ScraperOutput
import os 
import yaml 

def return_config_urls() -> str:
    print(os.getcwd())
    with open('./src/urls.yaml', 'r') as config:
        loaded_config = yaml.safe_load(config)

    return loaded_config['urls']


class ScrapeStaticData():


    def __init__(self):
        self.fetch_html_class = FetchHtml()
        self.parse_html_class = ParseHTML()
        self.urls = return_config_urls()
        self.scraper_data = {}

    


    def run_scraper(self):


        for site in self.urls:
            html = self.fetch_html_class.fetch_sites(site)

            self.parse_html_class.scrape_html(html)
            fetcher_results = self.fetch_html_class.result_list_fetcher
            parser_results = self.parse_html_class.result_list_parser
            
            self.scraper_data.update(fetcher_results)
            self.scraper_data.update(parser_results)

            scraper_output = ScraperOutput(self.scraper_data)
            scraper_output.scraper_json_output()

            self.scraper_data.clear()
            

            

