import time
from datetime import datetime
import uuid
from urllib.parse import urlparse
import requests
from log_data import log_events
from bs4 import BeautifulSoup


class FetchHtml():
    def __init__(self):
        self.max_tries = 3
        self.timeout = 5
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0'}
        self.status = ''
        self.unique_url = ''
        self.result_list_fetcher = {}


    def export_results(self):
        
        self.result_list_fetcher = {
            'unique_hash': self.unique_hash,
            'url': self.unique_url,
            'domain': self.domain,
            'date_scraped': self.date_scraped,
            'status': self.status
        }

            

    def fetch_sites(self, url):

        time_in_milliseconds = round(time.time() * 1000)


        try:
            self.unique_hash = uuid.uuid4()
            self.domain = urlparse(url).netloc
            self.date_scraped = datetime.now().isoformat()
            self.unique_url = url

            response = requests.get(url, allow_redirects=True, timeout=self.timeout, headers=self.user_agent)
            log_events(url,response.reason, time_in_milliseconds)

            if response.status_code == 200:
                print(f'success {self.domain}')
                self.status = 'success'
                self.export_results()
                return BeautifulSoup(response.content, 'html.parser') #return html to be parsed

            else:
                self.status = 'failed'
                for retry in range(self.max_tries):
                    response = requests.get(url, allow_redirects=True, timeout=self.timeout, headers=self.user_agent)
                    log_events(url,response.reason, time_in_milliseconds)
                    if response.status_code == 200:
                        self.status = 'success'
                        self.export_results()
                        return BeautifulSoup(response.content, 'html.parser') #return html to be parsed

                    #exponentional backoff
                    time.sleep(2 ** retry)
                
                self.export_results()
                                
        except requests.RequestException as error:
            self.status = 'failed'
            log_events(url, error , time_in_milliseconds)
            print(f'Error during request: {error}')
            self.export_results()


