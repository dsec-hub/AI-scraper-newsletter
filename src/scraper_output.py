
import orjson 


class ScraperOutput():
    def __init__(self, scraper_data:dict):
        for key, value in scraper_data.items():
            setattr(self, key, value)
        
        self.content_type = "Place Holder" #Pass LLM content_type here

    def scraper_json_output(self):
            
        json_schema = {
            'unique_hash': self.unique_hash,
            'unique_url': self.url,
            'domain': self.domain,
            'date_scraped': self.date_scraped,
            'content_type': self.content_type,
            'title': self.title,
            'author': self.author,
            'date_published': self.date_published,
            'clean_text': self.clean_text,
            'links': self.links,
            'status': self.status,
            'metadata': {
                'tags': self.tags,
                'raw_html_length': self.raw_html_length
            }
        }


        
        return print(orjson.dumps(json_schema).decode())