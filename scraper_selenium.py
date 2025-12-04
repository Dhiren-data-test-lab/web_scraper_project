# scraper_selenium.py
import yaml, logging, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils import save_to_csv, delay

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(path="config.yaml"):
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def make_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    return driver

def scrape_selenium(config_path="config.yaml"):
    cfg = load_config(config_path)
    driver = make_driver(headless=True)
    start = cfg["start_url"]
    driver.get(start)
    time.sleep(2)  # initial wait

    rows = []
    while True:
        soup = BeautifulSoup(driver.page_source, "lxml")
        items = soup.select(cfg["item"]["container_selector"])
        for it in items:
            row = {}
            for field, meta in cfg["item"]["fields"].items():
                sel = meta["selector"]
                attr = meta.get("attr", "text")
                node = it.select_one(sel)
                if not node:
                    row[field] = ""
                    continue
                if attr == "text":
                    row[field] = node.get_text(strip=True)
                else:
                    row[field] = node.get(attr, "")
                # absolute URLs could be fixed here if needed
            rows.append(row)

        # next button logic (simple)
        pag_sel = cfg.get("pagination", {}).get("selector")
        if not pag_sel:
            break
        next_el = driver.find_elements_by_css_selector(pag_sel)
        if next_el:
            try:
                next_el[0].click()
                time.sleep(cfg.get("delay_seconds", 2))
                continue
            except Exception as e:
                logger.info("Pagination click failed: " + str(e))
                break
        break

    driver.quit()
    if rows:
        save_to_csv(rows, cfg.get("output_csv", "output.csv"), list(rows[0].keys()))
    logger.info("Selenium scrape done.")

if __name__ == "__main__":
    scrape_selenium()
