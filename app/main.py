

import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.run import Scraper



def main():

    scrape_class = Scraper()
    scrape_class.run_scraper()



if __name__ == "__main__":
    main()