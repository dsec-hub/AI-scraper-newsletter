from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from app.utils import Logger
import time



class FetchSite:
    def fetch_site_text(url):
        with sync_playwright() as playwright:
            try:
                timer_started = round(time.time() * 1000) #time_in_milliseconds
                logger = Logger()
                
                browser = playwright.chromium.launch(headless=False)
                page = browser.new_page()
                response = page.goto(url=url, wait_until="domcontentloaded")
                
                site_html = page.content()
                html_parser = BeautifulSoup(site_html, "html.parser")
                stripped_html = html_parser.get_text(strip=True)

                logger.log_events(problem=response.status, url=url, time_in_milliseconds=timer_started)

                return stripped_html
            
            except Exception as error:
                logger.log_events(problem=response.status, url=url, time_in_milliseconds=timer_started)
                print(f"Fetch Site Error: {error}")


        
            