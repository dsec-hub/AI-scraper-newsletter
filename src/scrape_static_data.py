import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import orjson
import uuid
from datetime import datetime

class ScrapeStaticData():

    def __init__(self, urls):
        self.urls = urls
        self.content_type = ""
        self.unique_hash = None
        self.domain = ""
        self.date_now = ""
        self.user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"}

        self.clean_text = ""
        self.author = ""
        self.date_published = ""
        self.links = []
        self.tags = []
        self.raw_html_length = "" 


    def fetch_site(self, url, max_tries, timeout):
        self.unique_hash = uuid.uuid4()
        self.domain = urlparse(url).netloc
        self.date_now = datetime.now().isoformat()

        failed_urls = []
        for retry in range(max_tries):
            try:
                response = requests.get(url, allow_redirects=True, timeout=timeout, headers=self.user_agent)

                if response.status_code == 200:
                    print(f"success {self.domain}")
                    return BeautifulSoup(response.content, "html.parser")

                else:
                    failed_urls.append(set(url))
                    print("Failed to fetch page." \
                        f"HTTP Status Code: {response.status_code}." \
                        f"Domain: {self.domain}" \
                        "Retrying in {2 ** retry} seconds...")
                                                
                    #exponentional backoff
                    time.sleep(2 ** retry)
                
            except requests.RequestException as e:
                failed_urls.append(set(url))
                print(f"Error during request: {e}")
                return
        
        print(f"failed urls {failed_urls}")




    def fetch_urls(self):
        for url in self.urls:
            response = self.fetch_site(url, max_tries=3,
                                        timeout=5)


    


    def extract_text(self):
        html = self.fetch_site()

        #title




    def return_json_output(self):
        json_schema = {
            "id": self.unique_hash,
            "source_url": self.urls,
            "source_domain": self.domain,
            "scraped_at": self.date_now,
            "content_type": self.content_type,
            "title": "...",
            "author": "... or null",
            "published_date": "ISO string or null",
            "text": "clean text only",
            "links": ["https://..."],
            "metadata": {
                "tags": [],
                "raw_html_length": 12345
            }
        }

        return orjson.dumps(json_schema).decode()





class_instance = ScrapeStaticData(urls=[
    "https://daringfireball.net",
    "https://arstechnica.com",
    "https://theregister.com",
    "https://slashdot.org",
    "https://lwn.net",
    "https://hackernews.org",
    "https://tomshardware.com",
    "https://anandtech.com",
    "https://phoronix.com",
    "https://howtogeek.com",
    "https://ghacks.net",
    "https://osnews.com",
    "https://betanews.com",
    "https://techspot.com",
    "https://neowin.net"

])
class_instance.fetch_urls()
