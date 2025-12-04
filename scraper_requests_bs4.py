# scraper_requests_bs4.py
import yaml, logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import requests_session_with_retries, can_fetch, delay, save_to_csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def text_or_attr(elem, attr):
    if elem is None: return ""
    if attr == "text":
        return elem.get_text(strip=True)
    else:
        return elem.get(attr) or ""

def scrape(config_path="config.yaml"):
    cfg = load_config(config_path)
    start = cfg["start_url"]
    ua = cfg.get("user_agent")
    delay_s = cfg.get("delay_seconds", 1.0)
    session = requests_session_with_retries(cfg.get("max_retries", 3))
    session.headers.update({"User-Agent": ua})

    if not can_fetch(start, ua):
        logger.warning("robots.txt disallows scraping this URL. Aborting.")
        return

    url = start
    all_rows = []

    while url:
        logger.info(f"Fetching {url}")
        r = session.get(url, timeout=20)
        if r.status_code != 200:
            logger.warning(f"Status {r.status_code} for {url}")
            break
        soup = BeautifulSoup(r.content, "lxml")

        items = soup.select(cfg["item"]["container_selector"])
        for it in items:
            row = {}
            for field, meta in cfg["item"]["fields"].items():
                sel = meta["selector"]
                attr = meta.get("attr", "text")
                node = it.select_one(sel)
                val = text_or_attr(node, attr)
                if attr != "text" and val:
                    # make absolute urls if href/src
                    if attr in ("href", "src"):
                        val = urljoin(url, val)
                row[field] = val
            all_rows.append(row)

        # pagination
        pag_sel = cfg.get("pagination", {}).get("selector")
        if not pag_sel:
            break
        next_a = soup.select_one(pag_sel)
        if next_a and next_a.get("href"):
            url = urljoin(url, next_a.get("href"))
            delay(delay_s)
        else:
            break

    if all_rows:
        # write Excel (always good)
        from utils import save_to_xlsx, save_to_csv_utf16
        # overwrite the CSV file name from config (or use a safe default)
        out_csv = cfg.get("output_csv", "books_output.csv")
        # Write tab-separated UTF-16 CSV so Excel double-click opens correctly
        save_to_csv_utf16(all_rows, out_csv, list(all_rows[0].keys()))
        # Also write .xlsx (recommended)
        save_to_xlsx(all_rows, "books_output.xlsx", list(all_rows[0].keys()))

    logger.info("Done.")

if __name__ == "__main__":
    scrape()
