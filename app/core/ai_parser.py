from google import genai
import json
from dotenv import dotenv_values
import os
from urllib.parse import urlparse
import uuid
from datetime import datetime

class AIParser():
    def __init__(self):

        self.query_details = """{
                        url
                        title
                        author
                        date_published
                        content_type
                        clean_text (include only whats relevant for content_type)
                        tags
                        read_time_minutes
                }"""
        
        path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config'))
        self.config = dotenv_values(f"{path}/.env")

        self.ai_scrapper_results = {}



    def parse_text_to_json(self, site_text):
        
        try:
        
            client = genai.Client(api_key=self.config["GEMINI_API_KEY"])


            prompt=f"""
                You MUST respond with valid JSON only.
                From the following html collect the following. {self.query_details} {site_text}
                Never allow double quotation marks, always replace with single quotation marks Inside of clean_text.
                If you cannot see the html. You MUST say ERROR: Html Failed To Load. """

            response = client.models.generate_content(
                model="gemma-3-27b-it",
                contents=prompt,

            )

            ai_text = response.text

            print(ai_text)

            #Ai adds ```json prefix and ``` suffix by default. Must remove for json formatting.
            clean_ai_text = ( 
                ai_text
                .removeprefix("```json")
                .removesuffix("```")
                .strip()
            )

            scraped_at = datetime.now().isoformat()
            preliminary_ai_result = json.loads(clean_ai_text)


            source_domain = urlparse(preliminary_ai_result['url']).netloc
            site_id = str(uuid.uuid4())

            full_result = {
                "id":site_id,
                "domain": source_domain,
                "scraped_at": scraped_at,
                **preliminary_ai_result
            }

            return full_result
        
        except Exception as error:
            print(f"Ai Parser Error: {error}")
       