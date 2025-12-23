import requests
from bs4 import BeautifulSoup
from parse_html import ParseHTML


user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0'}

def give_html():
    response = requests.get('https://gcdb.com.au/article/gift-card-scams/', allow_redirects=True, timeout=5, headers=user_agent)

    proper_html = BeautifulSoup(response.content, 'html.parser')

    return proper_html



class_instance = ParseHTML

class_instance.scrape_html(give_html())