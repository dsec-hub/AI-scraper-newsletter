from google import genai
import json
from dotenv import dotenv_values
import os
from urllib.parse import urlparse
import uuid
from datetime import datetime
import sys


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
        
        config_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config'))
        self.env_config = dotenv_values(f"{config_path}/.env")

    @staticmethod
    def strip_code_fences(text: str) -> str:
        """Remove ``` ```json ``` fences if the model includes them."""
        return (
            text.removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )


    def build_prompt(self, article_text: dict) -> str:
        return f"""
                You MUST respond with valid JSON only.

                Task:
                - From the following site text, collect the following: {self.query_details}
                - Never allow double quotation marks, always replace with single quotation marks Inside of clean_text.
                - If you cannot see the site text. You MUST say ERROR: Site Text Failed To Load.
                
                Site Text:
                {article_text}
                """.strip()


    def parse_text_to_json(self, site_text):
        
        try:
        
            client = genai.Client(api_key=self.env_config["GEMINI_API_KEY"])


            prompt= self.build_prompt(site_text)

            response = client.models.generate_content(
                model="gemma-3-27b-it",
                contents=prompt,

            )

            clean_text = self.strip_code_fences(response.text or "")


            
            scraped_at = datetime.now().isoformat()
            preliminary_ai_result = json.loads(clean_text)

            source_domain = urlparse(preliminary_ai_result['url']).netloc
            site_id = str(uuid.uuid4())

            full_result = {
                "id":site_id,
                "domain": source_domain,
                "scraped_at": scraped_at,
                **preliminary_ai_result
            }

            return full_result
        
        except Exception:
            exc_type, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"{fname} File Error: Exception:{exc_type},  Line:{exc_tb.tb_lineno}")
       