import requests

API_URL = "http://127.0.0.1:5000/api/jobs"

job_data = {
    "title": "Actuary Analyst",
    "company": "Tech Corp",
    "location": "London",
    "posting_date": "2025-10-04T10:00:00",  # ISO 8601 format
    "job_type": "full-time",                 # must match ALLOWED_JOB_TYPES in backend
    "tags": "python, finance"
}

res = requests.post(API_URL, json=job_data)

if res.status_code == 201:
    print("Job saved successfully:", res.json())
else:
    print("Failed to save job:", res.status_code, res.text)
