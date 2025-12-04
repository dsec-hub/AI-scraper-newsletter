import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import orjson
import uuid
from datetime import datetime
import logging

class ScrapeStaticData():

    def __init__(self, urls):
        self.urls = urls
        self.content_type = ''
        self.unique_hash = None #populated by fetch site
        self.domain = '' #populated by fetch site
        self.date_now = ''#populated by fetch site
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0'}

        self.clean_text = '' #populated by extract_text
        self.author = '' #populated by extract_text
        self.title = '' #populated by extract_text
        self.date_published = '' #populated by extract_text
        self.links = []
        self.tags = []
        self.raw_html_length = '' 

        self.logging_config = logging.basicConfig(
                                filename='logs_url_event.log',
                                level=logging.DEBUG,
                                format='%(asctime)s - %(url)s - %(levelname)s - %(status)s - %(duration)s'
                              )

    def current_milli_time(self):
        return round(time.time() * 1000)

    def fetch_site(self, url, max_tries, timeout):
        self.unique_hash = uuid.uuid4()
        self.domain = urlparse(url).netloc
        self.date_now = datetime.now().isoformat()
        
        time_in_milliseconds = self.current_milli_time()

        failed_urls = []
        for retry in range(max_tries):
            try:
                response = requests.get(url, allow_redirects=True, timeout=timeout, headers=self.user_agent)

                if response.status_code == 200:
                    print(f'success {self.domain}')
                    self.return_json_output()
                    self.log_events(url,response.status_code, time_in_milliseconds)
                    soup= BeautifulSoup(response.content, 'html.parser')
                    self.extract_text(soup)


                else:
                    self.log_events(url,response.status_code, time_in_milliseconds)
                    print('Failed to fetch page.' \
                        f'HTTP Status Code: {response.status_code}.' \
                        f'Domain: {self.domain}' \
                        'Retrying in {2 ** retry} seconds...')
                                                
                    #exponentional backoff
                    time.sleep(2 ** retry)
                
            except requests.RequestException as e:
                self.log_events(url, e , time_in_milliseconds)
                print(f'Error during request: {e}')
                return
        
        print(f'failed urls {failed_urls}')




    def fetch_urls(self):
        for url in self.urls:
            self.fetch_site(url, max_tries=3,
                                        timeout=5)




    def log_events(self, problem, url, time_in_milliseconds):
        duration_end = self.current_milli_time()
        run_time_ms =  duration_end - time_in_milliseconds

        log_info = {
            'url': url,
            'status': problem,
            'duration': str(run_time_ms)+'ms',
        }

        logging.info("Logged Info", extra=log_info)
        



    def extract_text(self, soup):
        

        pass
        # html = self.fetch_site()

        #title






    def return_json_output(self):
        json_schema = {
            'id': self.unique_hash,
            'source_url': self.urls,
            'source_domain': self.domain,
            'scraped_at': self.date_now,
            'content_type': self.content_type,
            'title': self.title,
            'author': '... or null',
            'published_date': 'ISO string or null',
            'text': 'clean text only',
            'links': ['https://...'],
            'metadata': {
                'tags': [],
                'raw_html_length': 12345
            }
        }

        return print(orjson.dumps(json_schema).decode())





class_instance = ScrapeStaticData(urls=[
    'https://daringfireball.net',
    'https://arstechnica.com',
    'https://theregister.com',
    'https://slashdot.org',
    'https://lwn.net',
    'https://hackernews.org',
    'https://tomshardware.com',
    'https://anandtech.com',
    'https://phoronix.com',
    'https://howtogeek.com',
    'https://ghacks.net',
    'https://osnews.com',
    'https://betanews.com',
    'https://techspot.com',
    'https://neowin.net'

])
class_instance.fetch_urls()
