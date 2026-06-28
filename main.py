import os
from fastapi import FastAPI, Query, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from jobspy import scrape_jobs
import pandas as pd

app = FastAPI()
API_KEY = os.environ.get("JOBSPY_API_KEY")
API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(key: str = Security(api_key_header)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured on server")
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return key

@app.get("/jobs")
def get_jobs(
    keyword: str = Query(...),
    location: str = Query(default="India"),
    results: int = Query(default=50),
    remote_only: bool = Query(default=False),
    _: str = Security(verify_api_key)
):
    jobs = scrape_jobs(
        site_name=["linkedin", "indeed", "glassdoor"],
        search_term=keyword,
        location=location,
        results_wanted=results,
        is_remote=remote_only,
        country_indeed="India"
    )

    # Convert all date/datetime columns to strings
    for col in jobs.select_dtypes(include=["datetime", "datetimetz"]).columns:
        jobs[col] = jobs[col].astype(str)

    # Fill NaN and NaT with empty string, convert to dict
    jobs = jobs.fillna("").replace({pd.NaT: ""})

    return jobs.to_dict(orient="records")

@app.get("/health")
def health():
    return {"status": "ok"}
