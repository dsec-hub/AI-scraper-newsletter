from google import genai
import jsonlines
from dotenv import dotenv_values
import os
import yaml
from pathlib import Path

import sys

class Categorizer:

    def __init__(self):


        base_dir = Path(__file__).resolve().parent
        config_dir = (base_dir / ".." / "config").resolve()
        output_dir = (base_dir / ".." / ".." / "output").resolve()
        
        self.config_env = dotenv_values(config_dir / ".env")
        self.output_jsonl = output_dir / "articles.jsonl"

        if not self.output_jsonl.exists():
            raise FileNotFoundError(f"File:Categorizer.py, ERROR:Missing articles.jsonl file.")

        
        #load category labels to use.
        with open(f"{config_dir}/labels.yaml", 'r') as config_labels_file:
            loaded_labels = yaml.safe_load(config_labels_file)

        self.config_labels = loaded_labels['labels']

        
        self.fallback_output = {
            "id": " ",
            "categories": [],
            "needs_review": True,
        }

        api_key = self.config_env.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("File:Categorizer.py, ERROR:Missing GEMINI_API_KEY in config/.env")
        self.client = genai.Client(api_key=api_key)


        self.query_details = (
            f"Allowed categories: {self.config_labels}. "
            "Return categories as a LIST. Include confidence_scores."
        )

    @staticmethod
    def strip_code_fences(text: str) -> str:
        """Remove ``` ```json ``` fences if the model includes them."""
        return (
            text.removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )
        

    def build_prompt(self, article: dict) -> str:
        return f"""
                You MUST respond with valid JSON only.

                Task:
                - Determine which labels match the article's clean_text.
                - Provide confidence_scores as decimals (1.0 = 100%, 0.5 = 50%).
                - categories must include ONLY labels with confidence > 0.70.
                - If you cannot see/read the jsonl entry, output: "ERROR: jsonl Failed To Load."
                - If the entry is NONE, or if there are no qualifying categories, output EXACTLY this JSON:
                {self.fallback_output}

                {self.query_details}

                Article entry:
                {article}
                """.strip()

    def categorize_article(self):
        try:


            with jsonlines.open(self.output_jsonl) as articles_file:
                for article in articles_file:

                

                    prompt = self.build_prompt(article)

                    response = self.client.models.generate_content(
                        model="gemma-3-27b-it",
                        contents=prompt,
                    )

                    clean_text = self.strip_code_fences(response.text or "")
                    print(clean_text)
             


        except Exception:
            exc_type, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return(print(f"{fname} File Error: Exception:{exc_type},  Line:{exc_tb.tb_lineno}"))


class_instance = Categorizer()
class_instance.categorize_article()