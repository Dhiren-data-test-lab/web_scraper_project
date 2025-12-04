# 📘 Web Scraper Project (Sample Project-2)

A fully-functional, production-ready **Python Web Scraper** built for learning and freelancer portfolio use.  
It scrapes multiple pages, handles pagination, follows robots.txt rules, retries failed requests,  
and exports clean Excel files for real-world use.

This project is part of my **Freelancer Portfolio Series**,  
और इससे related कई advanced scrapers भी मेरे पास available हैं  
(e-commerce, news, job-scraper, PDF extraction, LinkedIn scraper etc.).

---

## 🚀 Features

- Scrapes data using **Requests + BeautifulSoup4**
- Handles **pagination (1–50 pages)** automatically
- Respects **robots.txt** (safe scraping)
- Automatic retry system (Connection errors पर)
- Clean extraction of:
  - **Title**
  - **Price**
  - **Rating**
  - **Product URL**
- Two output formats:
  - ✔ **books_output.xlsx (recommended)**
  - ✔ **books_output.csv (UTF-16 safe for Excel)**
- Clean encoding (No more `Â£` or special character issues)
- Config-driven system (`config.yaml`) — output name change कर सकते हैं

---

## 🧩 Project Structure

```
web_scraper_project/
│
├── scraper_requests_bs4.py    # Main scraper
├── scraper_selenium.py        # Selenium version (optional)
├── run_scrape.py              # Entry point
├── utils.py                   # Helper functions (retry, robots.txt, Excel writer)
├── config.yaml                # Configurable output settings
├── requirements.txt           # Install dependencies
├── books_output.xlsx          # Final Excel output
└── books_output.csv           # UTF-16 CSV (Excel safe)
```

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Scraper

```bash
python run_scrape.py
```

This will:

- scrape all pages (1 to N),
- create `books_output.xlsx`,
- and save the CSV as UTF-16.

---

## 📊 Output Preview

| title | price | rating | url |
|-------|--------|-----------|-----|
| A Light in the Attic | £51.77 | Three | https://… |
| Tipping the Velvet | £53.74 | One | https://… |
| … | … | … | … |

Excel screenshot included in repository.

---

## 🛠 Technologies Used

- Python 3  
- Requests  
- BeautifulSoup4  
- Pandas  
- YAML  
- Retry / HTTPAdapter  

---

## 📌 Notes

- Website used only for practice: **books.toscrape.com**  
- Scraper is safe and respects robots.txt  

---

## 📞 Need a Custom Web Scraper?

I can build:

- E-commerce price tracker  
- Job listing scraper  
- News/article scraper  
- Bulk PDF text extractor  
- Social media data scrapers  
- Excel automation scripts  
- Captcha handling (basic / advanced)  

👉 Contact me for custom projects.
