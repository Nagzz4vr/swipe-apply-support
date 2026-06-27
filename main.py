from fastapi import FastAPI, Query
from jobspy import scrape_jobs

app = FastAPI()

@app.get("/jobs")
def get_jobs(
    keyword: str = Query(...),
    location: str = Query(default="India"),
    results: int = Query(default=50),
    remote_only: bool = Query(default=False)
):
    jobs = scrape_jobs(
        site_name=["linkedin", "indeed", "glassdoor"],
        search_term=keyword,
        location=location,
        results_wanted=results,
        is_remote=remote_only,
        country_indeed="India"
    )
    return jobs.fillna("").to_dict(orient="records")
