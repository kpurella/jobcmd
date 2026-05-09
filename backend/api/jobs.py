from fastapi import APIRouter, HTTPException
from agents.tools import JobScannerTool, SAMPLE_JOBS
from agents.llm_client import LLMClient

router = APIRouter()

@router.get("/")
async def list_jobs():
    return {"jobs": SAMPLE_JOBS, "total": len(SAMPLE_JOBS)}

@router.get("/scan")
async def scan_jobs(keywords: str = ""):
    scanner = JobScannerTool()
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
    return await scanner.run({"keywords": kw_list}, {})

@router.post("/match")
async def match_jobs(data: dict):
    profile = data.get("profile", {})
    provider = data.get("provider", "anthropic")
    llm = LLMClient(provider=provider)
    results = []
    for job in SAMPLE_JOBS:
        match = await llm.match_job(job, profile)
        job_copy = dict(job)
        job_copy.update(match)
        results.append(job_copy)
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return {"matched": results}

@router.get("/{job_id}")
async def get_job(job_id: str):
    job = next((j for j in SAMPLE_JOBS if j["id"] == job_id), None)
    if not job: raise HTTPException(404, "Job not found")
    return job
