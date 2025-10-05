# Scrapper/scrape.py
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

API_URL = "http://127.0.0.1:5000/api/jobs"
MAX_RETRIES = 3  # retry POST requests if backend fails

def safe_text(element):
    try:
        return element.text.strip()
    except:
        return ""

def post_job(job_data):
    for attempt in range(MAX_RETRIES):
        try:
            res = requests.post(API_URL, json=job_data)
            if res.status_code == 201:
                print(f"[SUCCESS] Saved: {job_data['title']}")
                return True
            else:
                print(f"[FAILED] {job_data['title']}: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"[ERROR] {job_data['title']} POST attempt {attempt+1}: {e}")
        time.sleep(1)
    return False

def run():
    options = Options()
    # options.headless = True  # Uncomment to run headless
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.actuarylist.com")

    # Wait for job cards
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//article//div[contains(@class,'Job_job-card')]"))
    )

    # Scroll to load all jobs
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    job_cards = driver.find_elements(By.XPATH, "//article//div[contains(@class,'Job_job-card')]")
    print(f"Found {len(job_cards)} jobs")

    for job in job_cards[:10]:  # Limit for testing
        try:
            # Title
            try:
                title_elem = WebDriverWait(job, 5).until(
                    EC.presence_of_element_located((By.XPATH, ".//p[1]"))
                )
                title = safe_text(title_elem)
            except:
                title = "N/A"

            # Company
            try:
                company_elem = job.find_element(By.XPATH, ".//p[2]")
                company = safe_text(company_elem)
            except:
                company = "N/A"

            # Locations
            try:
                locations = [safe_text(loc) for loc in job.find_elements(By.XPATH, ".//div[contains(@class,'locations')]//a")]
            except:
                locations = []

            # Tags
            try:
                tags = [safe_text(tag) for tag in job.find_elements(By.XPATH, ".//div[contains(@class,'tags')]//a")]
            except:
                tags = []

            # Posting date
            try:
                posting_date_elem = job.find_element(By.XPATH, ".//p[last()]")
                posting_date_text = safe_text(posting_date_elem)
                try:
                    posting_date = datetime.strptime(posting_date_text, "%d %b %Y").isoformat()
                except:
                    posting_date = posting_date_text
            except:
                posting_date = "N/A"

            if title == "N/A" or company == "N/A":
                print(f"[SKIPPED] Missing title/company, skipping job.")
                continue

            job_data = {
                "title": title,
                "company": company,
                "locations": ", ".join(locations),  # Convert list to string for backend safety
                "posting_date": posting_date,
                "tags": ", ".join(tags),  # Convert list to string
                "job_type": "full-time"
            }

            post_job(job_data)

        except Exception as e:
            print(f"[ERROR] Failed to scrape a job: {e}")

    driver.quit()

if __name__ == "__main__":
    run()
