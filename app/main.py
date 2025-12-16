from .core import ScrapeStaticData


def main():
    #code to check if site is static or dynamic

    #call class if static
    static_scrape_class = ScrapeStaticData()
    static_scrape_class.run_scraper()

    #call class if dynamic

if __name__ == "__main__":
    main()