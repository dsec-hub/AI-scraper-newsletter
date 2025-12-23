import jsonlines
import os.path



class ScraperOutput:

    def save(data: dict) -> None:
            
        # Source: https://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
        # Author: forivall
        # License: CC BY-SA 4.0   
        path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'output'))

        if os.path.exists(path) == False:
            os.mkdir(path)
            
        with jsonlines.open(f'{path}/article.jsonl', mode='a') as article_records:
            article_records.write(str(data))
        
        return 
