from playwright.sync_api import sync_playwright
from google import genai
import json
from dotenv import dotenv_values
from bs4 import BeautifulSoup
import uuid 
from datetime import datetime
from urllib.parse import urlparse
from log_data import log_events
import time

class ScrapeData():
    def __init__(self):

        self.query_details = """{
                        url
                        title
                        author
                        date_published
                        content_type
                        clean_text (include only whats relevant for content_type)
                        links
                        tags
                        raw_html_length
                }"""
        
        self.config = dotenv_values("./src/.env")

        self.export_ai_result_json = {}
        self.ai_scrapper_results = {}


    def export_results(self):
        self.unique_hash = str(uuid.uuid4())
        self.date_scraped = datetime.now().isoformat()
        self.domain = urlparse(self.ai_scrapper_results['url']).netloc
        self.export_ai_result_json = {
            'unique_hash': self.unique_hash,
            'url': self.ai_scrapper_results['url'],
            'domain': self.domain,
            'date_scraped': self.date_scraped,
            'content_type': self.ai_scrapper_results['content_type'],
            'title': self.ai_scrapper_results['title'],
            'author': self.ai_scrapper_results['author'],
            'date_published': self.ai_scrapper_results['date_published'],
            'clean_text': self.ai_scrapper_results['clean_text'],
            'links': self.ai_scrapper_results['links'],
            'tags': self.ai_scrapper_results['tags'],
            'raw_html_length': self.ai_scrapper_results['raw_html_length'],
        }
        print(self.export_ai_result_json)

    def html_ai_scraper(self, query, html):
        config = dotenv_values("./src/.env")
        client = genai.Client(api_key=config["GEMINI_API_KEY"])


        prompt=f"""
            You MUST respond with valid JSON only.
            From the following html collect the following. {query} {html}
            Never allow double quotation marks, always replace with single quotation marks Inside of clean_text.
            If you cannot see the html. You MUST say ERROR: Html Failed To Load. """

        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt,

        )

        ai_text = response.text

        print(ai_text)

        clean_ai_text = ( #ai adds prefix and suffix as its formatting. Must remove.
            ai_text
            .removeprefix("```json")
            .removesuffix("```")
            .strip()
        )

        result = json.loads(clean_ai_text)
        self.ai_scrapper_results.update(result)




    def scrape_data(self, url):
        time_in_milliseconds = round(time.time() * 1000)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            
            page = browser.new_page()

            
            response = page.goto(url=url, wait_until="domcontentloaded")
            log_events(problem=response.status, url=url, time_in_milliseconds=time_in_milliseconds)
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            stripped_html = soup.get_text(strip=True)



            self.html_ai_scraper(self.query_details, stripped_html)
            self.export_results()
                
