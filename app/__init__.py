# Import key classes and functions for easier access
from .core.fetch_html import FetchHtml
from .core.parse_html import ParseHTML
from .core.scrape_static_data import ScrapeStaticData
from .core.scraper_output import ScraperOutput
from .utils.log_data import Logger

# Define the public API of the package
__all__ = [
    "FetchHtml",
    "ParseHTML",
    "ScrapeStaticData",
    "ScraperOutput",
    "Logger",
]