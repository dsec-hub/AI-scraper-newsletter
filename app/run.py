from .core import FetchHtml
from .core import ParseHTML
from .core import ScraperOutput
from .core import LLM_Enrich
import os 
import yaml 

def return_config_urls() -> str:
    print(os.getcwd())
    with open('./app/config/urls.yaml', 'r') as config:
        loaded_config = yaml.safe_load(config)

    return loaded_config['urls']


class Scraper:
    def __init__(self):
        self.fetch_html_class = FetchHtml()
        self.parse_html_class = ParseHTML()
        self.LLM_enrich_class = LLM_Enrich
        self.urls = return_config_urls()

    def run_scraper(self):


        for site in self.urls:
            html = self.fetch_html_class.fetch_sites(site)

            if html['success'] == False: #skip url if exception error
                continue

            parsed_info = self.parse_html_class.scrape_html(html['html'])
            
            self.LLM_enrich_class.enrich(data=parsed_info['text'])


            scraper_output = ScraperOutput
            scraper_output.save(data=parsed_info)
            

            

