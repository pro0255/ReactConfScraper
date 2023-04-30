import requests
from bs4 import BeautifulSoup
from scraper import Scraper
from config import URL_JS_NOTION, URL_REACT_SUMMIT

notion_scraper = Scraper(URL_JS_NOTION) 
summit_scraper = Scraper(URL_REACT_SUMMIT)


instances = [notion_scraper, summit_scraper]

[instane.scrape() for instane in instances]
