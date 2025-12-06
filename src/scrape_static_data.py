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
                    soup = BeautifulSoup(response.content, 'html.parser')      
                    self.extract_text(soup)                                    
                    self.return_json_output()                                  
                    self.log_events(url, response.status_code, time_in_milliseconds)
                    return soup



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

        self.raw_html_length = len(str(soup)) # sets raw_html_length var to length of soup(parsed html's len)

        title = ""

        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title and og_title.get("content"):
            title = og_title["content"].strip()

        if not title and soup.title and soup.title.string:
            title = soup.title.string.strip()

        if not title:
            h1 = soup.find("h1")
            if h1:
                title = h1.get_text(" ", strip=True)

        self.title = title

        main_container = soup.find("article")
        if main_container is None:
            main_container = soup.find("main")

        if main_container is None:
            main_container = soup.find(
                "div",
                attrs={"id": lambda v: isinstance(v, str) and "content" in v.lower()},
            )

        if main_container is None:
            main_container = soup.find(
                "div",
                attrs={"class": lambda v: isinstance(v, str) and "content" in v.lower()},
            )

        paragraphs = []

        if main_container:
            paragraph_nodes = main_container.find_all("p")
        else:
            paragraph_nodes = soup.find_all("p")

        for p in paragraph_nodes:
            text = p.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)

        text_joined = "\n\n".join(paragraphs)

        if not text_joined or len(text_joined.split()) < 50:
            if main_container:
                fallback_text = main_container.get_text(" ", strip=True)
                if fallback_text and len(fallback_text.split()) > len(text_joined.split()):
                    text_joined = fallback_text

        if not text_joined:
            whole_page_text = soup.get_text(" ", strip=True)
            if whole_page_text:
                text_joined = whole_page_text

        self.clean_text = text_joined

        if main_container:
            link_nodes = main_container.find_all("a", href=True)
        else:
            link_nodes = soup.find_all("a", href=True)

        links = []
        for a in link_nodes:
            href = a["href"].strip()
            if href:
                links.append(href)

        self.links = links

        author = ""

        meta_author = soup.find("meta",attrs={"name": "author"})
        if meta_author and meta_author.get("content"):
            author = meta_author["content"].strip()

        if not author:
            meta_author = soup.find("meta",attrs={"property": "article:author"})
            if meta_author and meta_author.get("content"):
                author = meta_author["content"].strip()

        if not author:
            byline = soup.find(
                attrs={
                    "class": lambda v: (
                        isinstance(v, str)
                        and ("author" in v.lower() or "byline" in v.lower())
                    )
                }
            )
            if byline:
                author = byline.get_text(" ", strip=True)

        self.author = author

        date_value = ""

        date_meta_candidates = [
            {"property": "article:published_time"},
            {"name": "pubdate"},
            {"name": "date"},
            {"name": "DC.date.issued"},
        ]

        for attrs in date_meta_candidates:
            meta = soup.find("meta", attrs=attrs)
            if meta and meta.get("content"):
                date_value = meta["content"].strip()
                break

        if not date_value:
            time_tag = soup.find("time")
            if time_tag:
                datetime_attr = time_tag.get("datetime")
                if datetime_attr:
                    date_value = datetime_attr.strip()
                else:
                    date_value = time_tag.get_text(" ", strip=True)

        self.date_published = date_value

        tags = []
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        if meta_keywords and meta_keywords.get("content"):
            raw_keywords = meta_keywords["content"]
            tags = [kw.strip() for kw in raw_keywords.split(",") if kw.strip()]

        self.tags = tags

        word_count = len(self.clean_text.split())
        if word_count > 0:
            self.read_time_minutes = max(1, round(word_count / 200))
        else:
            self.read_time_minutes = 0


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
