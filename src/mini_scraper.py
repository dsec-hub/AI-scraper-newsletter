from bs4 import BeautifulSoup
import requests


response=requests.get('https://daringfireball.net')
html_code=response.content
soup=BeautifulSoup(html_code,"html.parser")
readable_soup=soup.prettify()
str_readable_soup=str(readable_soup)

title=soup.find("title")
with open("html-1.html","w") as file:
    file.write(str_readable_soup)
h1=soup.find("h1")

if title==None:
    print(h1)


