"""Agent Tools - scanner, matcher, document generator, applicator"""
import asyncio, uuid, datetime
from typing import Dict, List, Any

SAMPLE_JOBS = [
    {"id": "job_001", "title": "Senior Software Engineer", "company": "TechCorp", "location": "Remote",
     "salary_min": 150000, "salary_max": 200000,
     "description": "Build scalable backend systems with Python and Go. Lead a team of 5 engineers. Own services handling 10M req/day.",
     "requirements": ["Python", "Go", "AWS", "PostgreSQL", "5+ years"], "source": "Greenhouse",
     "url": "https://greenhouse.io/jobs/001", "posted_at": "2025-04-25"},
    {"id": "job_002", "title": "ML Engineer", "company": "AI Startup", "location": "San Francisco, CA",
     "salary_min": 160000, "salary_max": 220000,
     "description": "Design and deploy ML pipelines at scale. Work with LLMs and computer vision. Own the full ML lifecycle.",
     "requirements": ["Python", "PyTorch", "MLflow", "Kubernetes", "3+ years"], "source": "Workday",
     "url": "https://workday.com/jobs/002", "posted_at": "2025-04-27"},
    {"id": "job_003", "title": "Full Stack Developer", "company": "FinTech Co", "location": "New York, NY",
     "salary_min": 130000, "salary_max": 170000,
     "description": "Build financial dashboards and trading interfaces. React frontend, Node.js backend, real-time data.",
     "requirements": ["React", "Node.js", "TypeScript", "PostgreSQL", "REST APIs"], "source": "LinkedIn",
     "url": "https://linkedin.com/jobs/003", "posted_at": "2025-04-26"},
    {"id": "job_004", "title": "DevOps Engineer", "company": "CloudScale", "location": "Remote",
     "salary_min": 140000, "salary_max": 190000,
     "description": "Manage Kubernetes clusters and CI/CD pipelines. 99.99% uptime SLA. On-call rotation.",
     "requirements": ["Kubernetes", "Terraform", "AWS", "Python", "Linux"], "source": "Greenhouse",
     "url": "https://greenhouse.io/jobs/004", "posted_at": "2025-04-24"},
    {"id": "job_005", "title": "Product Manager - AI", "company": "Enterprise SaaS", "location": "Austin, TX",
     "salary_min": 145000, "salary_max": 195000,
     "description": "Drive AI product strategy. Work with LLM teams and enterprise customers. 0 to 1 product ownership.",
     "requirements": ["Product Management", "AI/ML", "SQL", "Stakeholder Management", "3+ years PM"], "source": "Workday",
     "url": "https://workday.com/jobs/005", "posted_at": "2025-04-28"},
    {"id": "job_006", "title": "Data Engineer", "company": "DataOps Inc", "location": "Remote",
     "salary_min": 120000, "salary_max": 160000,
     "description": "Build data pipelines and warehouses. Spark, Airflow, Snowflake stack. 5PB data lake.",
     "requirements": ["Python", "Spark", "Airflow", "Snowflake", "dbt"], "source": "Lever",
     "url": "https://lever.co/jobs/006", "posted_at": "2025-04-23"},
    {"id": "job_007", "title": "Backend Engineer - Rust", "company": "Systems Co", "location": "Remote",
     "salary_min": 170000, "salary_max": 230000,
     "description": "Write high-performance Rust services. Low-latency trading systems. Memory-safe systems programming.",
     "requirements": ["Rust", "C++", "Linux", "gRPC", "Distributed Systems"], "source": "Greenhouse",
     "url": "https://greenhouse.io/jobs/007", "posted_at": "2025-04-22"},
    {"id": "job_008", "title": "AI Research Engineer", "company": "DeepMind Labs", "location": "London, UK (Hybrid)",
     "salary_min": 155000, "salary_max": 210000,
     "description": "Research and implement novel ML architectures. Publish papers. Work on frontier AI safety problems.",
     "requirements": ["Python", "JAX", "PyTorch", "Research Background", "PhD preferred"], "source": "Direct",
     "url": "https://deepmind.com/jobs/008", "posted_at": "2025-04-29"},
]

class JobScannerTool:
    async def run(self, params: Dict, profile: Dict) -> Dict:
        await asyncio.sleep(0.3)
        keywords = [k.lower() for k in params.get("keywords", [])]
        jobs = []
        for j in SAMPLE_JOBS:
            j_copy = dict(j)
            if keywords:
                reqs_text = " ".join(j["requirements"]).lower()
                hits = sum(1 for k in keywords if k in reqs_text)
                j_copy["keyword_hits"] = hits
            else:
                j_copy["keyword_hits"] = 0
            jobs.append(j_copy)
        jobs.sort(key=lambda x: x.get("keyword_hits", 0), reverse=True)
        return {"jobs_found": len(jobs), "jobs": jobs,
                "sources_scanned": ["Greenhouse", "Workday", "LinkedIn", "Lever", "Direct"]}

class MatcherTool:
    def __init__(self, llm_client):
        self.llm = llm_client

    async def run(self, params: Dict, profile: Dict) -> Dict:
        threshold = params.get("threshold", 0.6)
        matched = []
        for job in SAMPLE_JOBS:
            match_result = await self.llm.match_job(job, profile)
            job_copy = dict(job)
            job_copy["match_score"] = match_result.get("score", 50) / 100
            job_copy["match_reasoning"] = match_result.get("reasoning", "")
            job_copy["match_strengths"] = match_result.get("strengths", [])
            job_copy["match_gaps"] = match_result.get("gaps", [])
            if job_copy["match_score"] >= threshold:
                matched.append(job_copy)
        matched.sort(key=lambda x: x["match_score"], reverse=True)
        return {"matched_count": len(matched), "jobs": matched}

class DocumentGeneratorTool:
    def __init__(self, llm_client):
        self.llm = llm_client

    async def run(self, params: Dict, profile: Dict) -> Dict:
        top_n = params.get("top_n", 3)
        docs = []
        for job in SAMPLE_JOBS[:top_n]:
            letter = await self.llm.generate_cover_letter(job, profile)
            docs.append({
                "job_id": job["id"], "job_title": job["title"], "company": job["company"],
                "cover_letter": letter, "generated_at": datetime.datetime.utcnow().isoformat()
            })
        return {"generated": len(docs), "documents": docs}

class ApplicationTool:
    async def run(self, params: Dict, profile: Dict) -> Dict:
        await asyncio.sleep(0.8)
        return {
            "job_id": params.get("job_id", ""),
            "status": "applied",
            "method": "browser_automation_playwright",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "confirmation_id": f"APP-{uuid.uuid4().hex[:8].upper()}"
        }
