
class ParseHTML():
    def __init__(self):
        self.title = ''
        self.author = ''
        self.date_published = ''
        self.clean_text = ''
        self.links = []
        self.tags = []
        self.raw_html_length = '' 

        self.result_list_parser = {}


    def export_results(self):
        self.result_list_parser =  {
                'title': self.title,
                'author': self.author,
                'date_published': self.date_published,
                'clean_text': self.clean_text,
                'links': self.links,
                'tags': self.tags,
                'raw_html_length': self.raw_html_length,
            }
        

    def scrape_html(self, html):
             
            if html is None: #check if fetcher had an exception/error
                self.title = ''
                self.author = ''
                self.date_published = ''
                self.clean_text = ''
                self.links = []
                self.tags = []
                self.raw_html_length = '' 
                self.export_results() #needed to prevent outputing previous results.
                return 'Cannot Parse Html due to error Fetching.'
            
            self.raw_html_length = len(str(html)) 

            title = ""

            og_title = html.find("meta", attrs={"property": "og:title"})
            if og_title and og_title.get("content"):
                title = og_title["content"].strip()

            if not title and html.title and html.title.string:
                title = html.title.string.strip()

            if not title:
                h1 = html.find("h1")
                if h1:
                    title = h1.get_text(" ", strip=True)

            self.title = title

            main_container = html.find("article")
            if main_container is None:
                main_container = html.find("main")

            if main_container is None:
                main_container = html.find(
                    "div",
                    attrs={"id": lambda v: isinstance(v, str) and "content" in v.lower()},
                )

            if main_container is None:
                main_container = html.find(
                    "div",
                    attrs={"class": lambda v: isinstance(v, str) and "content" in v.lower()},
                )

            paragraphs = []


            pass
            if main_container:
                paragraph_nodes = main_container.find_all("p")
            else:
                paragraph_nodes = html.find_all("p")


            #title
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
                whole_page_text = html.get_text(" ", strip=True)
                if whole_page_text:
                    text_joined = whole_page_text

            self.clean_text = text_joined

            if main_container:
                link_nodes = main_container.find_all("a", href=True)
            else:
                link_nodes = html.find_all("a", href=True)

            links = []
            for a in link_nodes:
                href = a["href"].strip()
                if href:
                    links.append(href)

            self.links = links

            author = ""

            meta_author = html.find("meta",attrs={"name": "author"})
            if meta_author and meta_author.get("content"):
                author = meta_author["content"].strip()

            if not author:
                meta_author = html.find("meta",attrs={"property": "article:author"})
                if meta_author and meta_author.get("content"):
                    author = meta_author["content"].strip()

            if not author:
                byline = html.find(
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
                meta = html.find("meta", attrs=attrs)
                if meta and meta.get("content"):
                    date_value = meta["content"].strip()
                    break

            if not date_value:
                time_tag = html.find("time")
                if time_tag:
                    datetime_attr = time_tag.get("datetime")
                    if datetime_attr:
                        date_value = datetime_attr.strip()
                    else:
                        date_value = time_tag.get_text(" ", strip=True)


            self.date_published = date_value


            tags = []
            meta_keywords = html.find("meta", attrs={"name": "keywords"})
            if meta_keywords and meta_keywords.get("content"):
                raw_keywords = meta_keywords["content"]
                tags = [kw.strip() for kw in raw_keywords.split(",") if kw.strip()]


            self.tags = tags


            word_count = len(self.clean_text.split())
            if word_count > 0:
                self.read_time_minutes = max(1, round(word_count / 200))
            else:
                self.read_time_minutes = 0



            
            self.export_results()

