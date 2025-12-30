
from .core import AIParser
from .core import ScraperOutput
from .core import FetchSite
import os 
import yaml 

def return_config_urls() -> str:
    print(os.getcwd())
    with open('./app/config/urls.yaml', 'r') as config:
        loaded_config = yaml.safe_load(config)

    return loaded_config['urls']


class Scraper:
    def __init__(self):
        self.fetch_site_class = FetchSite
        self.ai_parser_class = AIParser()

        self.urls = return_config_urls()

    def run_scraper(self):


        for site in self.urls:
            text = self.fetch_site_class.fetch_site_text(site)

            parsed_info = self.ai_parser_class.parse_text_to_json(text)

            scraper_output = ScraperOutput
            scraper_output.save(data=parsed_info)
            

            

