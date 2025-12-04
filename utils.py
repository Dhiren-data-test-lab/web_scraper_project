import time, csv, sqlite3, logging
import requests
from urllib.parse import urljoin, urlparse
import urllib.robotparser
from requests.adapters import HTTPAdapter, Retry
import pandas as pd    # for xlsx export

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def can_fetch(url, user_agent):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except:
        return True
    return rp.can_fetch(user_agent, url)

def requests_session_with_retries(total_retries=3, backoff=0.3):
    s = requests.Session()
    retries = Retry(total=total_retries,
                    backoff_factor=backoff,
                    status_forcelist=[429,500,502,503,504],
                    allowed_methods=frozenset(['GET','POST']))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))
    return s


# ----------------------------------------------------------
# SAVE CSV  (UTF-8-SIG → Excel-safe, no Â symbol)
# ----------------------------------------------------------
def save_to_csv(rows, path, fieldnames):
    """
    Writes rows to CSV using UTF-8 with BOM so that Excel 
    reads currency symbols (like £) correctly without Â.
    """
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    logger.info(f"Saved {len(rows)} rows to {path}")
# ----------------------------------------------------------
# SAVE CSV as UTF-16 with BOM (tab-separated) — Excel-friendly on double-click
# ----------------------------------------------------------
def save_to_csv_utf16(rows, path, fieldnames, delimiter="\t"):
    """
    Write rows (list of dicts) to a tab-separated CSV encoded as UTF-16 with BOM.
    Excel on Windows reliably opens this correctly when double-clicked.
    """
    if not rows:
        logger.info("No rows to save (utf16).")
        return
    # use encoding 'utf-16' so Python writes BOM automatically (platform little-endian)
    with open(path, "w", newline="", encoding="utf-16") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)
    logger.info(f"Saved {len(rows)} rows to {path} (UTF-16, delimiter={repr(delimiter)})")



# ----------------------------------------------------------
# SAVE XLSX  (Perfect for Excel users → Clean columns)
# ----------------------------------------------------------
def save_to_xlsx(rows, path, fieldnames=None):
    """
    rows: list of dicts.
    path: 'books_output.xlsx'
    """
    if not rows:
        print("No rows to save")
        return
    df = pd.DataFrame(rows)
    if fieldnames:
        df = df.reindex(columns=fieldnames)
    df.to_excel(path, index=False, engine="openpyxl")
    print(f"Saved {len(rows)} rows to {path}")


def delay(seconds):
    time.sleep(seconds)
