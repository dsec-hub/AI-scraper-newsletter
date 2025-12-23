import time
import requests
from app.utils import Logger
from bs4 import BeautifulSoup


class FetchHtml:
    def __init__(self):
        self.max_tries = 3
        self.timeout = 5
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0'}



    def fetch_sites(self, url):
        logger = Logger()
        time_in_milliseconds = round(time.time() * 1000)

        for retry in range(self.max_tries):
            try:
                response = requests.get(url, allow_redirects=True, timeout=self.timeout, headers=self.user_agent)
                logger.log_events(url,response.reason, time_in_milliseconds)

                html = BeautifulSoup(response.content, 'html.parser')
                if response.status_code == 200: #200 represents valid response 
                    print(f'success {url}')
                    return {
                        "success": True,
                        "html": html,
                        "status_code": response.status_code,
                    }
                
                #exponentional backoff
                time.sleep(2 ** retry)
                  
            except requests.RequestException as error:
                logger.log_events(url, error , time_in_milliseconds)
                print(f'Error during request: {error}')



        return {
            "success": False,
            "html": None,
            "status_code": None,
        }
