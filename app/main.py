from .run import Scraper


def main():
    #code to check if site is static or dynamic

    #call class if static
    scrape_class = Scraper()
    scrape_class.run_scraper()

    #call class if dynamic

if __name__ == "__main__":
    main()