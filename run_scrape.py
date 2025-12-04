# run_scrape.py
import yaml
from scraper_requests_bs4 import scrape as scrape_requests
from scraper_selenium import scrape_selenium

cfg = yaml.safe_load(open("config.yaml"))
if cfg.get("use_selenium"):
    scrape_selenium()
else:
    scrape_requests()
