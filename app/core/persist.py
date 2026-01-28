import jsonlines
import os.path
import sys


class ScraperOutput:

    def save(data: dict) -> None:
        try:
            
            # Source: https://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
            # Author: forivall
            # License: CC BY-SA 4.0   
            path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'output'))

            if os.path.exists(path) == False:
                os.mkdir(path)
            
            if not data:
                return False
            
                
            with jsonlines.open(f'{path}/articles.jsonl', mode='a') as article_records:
                article_records.write(str(data))
             
        
        except Exception:
            exc_type, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"{fname} File Error: Exception:{exc_type},  Line:{exc_tb.tb_lineno}")
