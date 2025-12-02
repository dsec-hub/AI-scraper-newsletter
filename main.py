import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import orjson
import uuid
from datetime import datetime

class ScrapeData():

    def __init__(self, url):
        self.results = []
        self.url = url
        self.content_type = ""
        self.unique_hash = uuid.uuid4()
        self.domain = urlparse(self.url).netloc
        self.date_now = datetime.now().isoformat()


    def fetch_site(self):
        try:
            max_tries = 3
            for retry in range(max_tries):
                response = requests.get(self.url, allow_redirects=True, timeout=5)

                if response.status_code == 200:
                    break

                else:
                    print(f"Failed to fetch page."
                        "HTTP Status Code: {response.status_code}." \
                        "Retrying in {2 ** retry} seconds...")
                    
                    #exponentional backoff
                    time.sleep(2 ** retry)

            assert response.status_code == 200, (f"Unable To Fetch Site." 
                                                "HTTP Status Code:  {response.status_code}")
            

            html = BeautifulSoup(response.content, "html.parser")

            return html

        except requests.RequestException as e:
            print(f"Error during request: {e}")
            return
    

    def extract_text(self):
        html = self.fetch_site()


    def return_json_output(self):
        json_schema = {
            "id": self.unique_hash,
            "source_url": self.url,
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



if __name__ == "__main__":
    class_instance = ScrapeData("https://ia.acs.org.au/article/2025/optus-blames-copper-thieves-for-mobile-service-outage.html")
    class_instance.fetch_site()
