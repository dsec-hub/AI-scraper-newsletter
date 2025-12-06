import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import orjson
import uuid
from datetime import datetime
import log_data
import yaml

class ScrapeStaticData():


    def __init__(self, urls):
        self.urls = urls
        self.content_type = ''
        self.unique_hash = None
        self.domain = ''
        self.date_now = ''
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0'}


        self.clean_text = ''
        self.author = ''
        self.title = ''
        self.date_published = ''
        self.links = []
        self.tags = []
        self.raw_html_length = '' 



    
    def current_milli_time(self):
        return round(time.time() * 1000)
    
    def set_site_attributes(self, url_given):
        self.unique_hash = uuid.uuid4()
        self.domain = urlparse(url_given).netloc
        self.date_now = datetime.now().isoformat()

    def fetch_site(self, url, max_tries, timeout):
        self.set_site_attributes(url)
        
        time_in_milliseconds = self.current_milli_time()


        for retry in range(max_tries):
            try:
                response = requests.get(url, allow_redirects=True, timeout=timeout, headers=self.user_agent)

                if response.status_code == 200:
                    print(f'success {self.domain}')
                    self.scraper_json_output(url)
                    log_data.log_events(url,response.reason, time_in_milliseconds)
                    return BeautifulSoup(response.content, 'html.parser')

                else:
                    log_data.log_events(url,response.reason, time_in_milliseconds)
                    print('Failed to fetch page.' \
                        f'HTTP Status Code: {response.status_code}.' \
                        f'Domain: {self.domain}' \
                        'Retrying in {2 ** retry} seconds...')
                                                
                    #exponentional backoff
                    time.sleep(2 ** retry)
                
            except requests.RequestException as e:
                log_data.log_events(url, e , time_in_milliseconds)
                print(f'Error during request: {e}')
                return
        



    def fetch_urls(self):
        for url in self.urls:
            self.fetch_site(url, max_tries=3,
                                        timeout=5)


    def extract_text(self):

        pass
        # html = self.fetch_site()

        #title


    def scraper_json_output(self, url):
         
        json_schema = {
            'id': self.unique_hash,
            'source_url': url,
            'source_domain': self.domain,
            'scraped_at': self.date_now,
            'content_type': self.content_type,
            'title': self.title,
            'author': self.author,
            'published_date': self.date_published,
            'text': self.clean_text,
            'links': self.links,
            'metadata': {
                'tags': self.tags,
                'raw_html_length': self.raw_html_length
            }
        }

        with open('../logs/scraper_json_output.json', 'a') as scraper_output:
            scraper_output.write(f"{orjson.dumps(json_schema).decode()}\n\n")



def return_config_urls():
    with open('urls.yaml', 'r') as config:
        loaded_config = yaml.safe_load(config)

    return loaded_config['urls']



class_instance = ScrapeStaticData(urls=return_config_urls())
class_instance.fetch_urls()
