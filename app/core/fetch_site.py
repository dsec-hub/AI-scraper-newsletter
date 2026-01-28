from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from app.utils import Logger
import time
import os
import sys



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
            
            except Exception:
                logger.log_events(problem=response.status, url=url, time_in_milliseconds=timer_started)
                exc_type, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(f"{fname} File Error: Exception:{exc_type},  Line:{exc_tb.tb_lineno}")


        
            