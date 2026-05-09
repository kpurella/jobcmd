from fastapi import APIRouter
from agents.llm_client import LLMClient
from agents.planner import PlannerAgent

router = APIRouter()

@router.post("/run")
async def run_agent(data: dict):
    goal = data.get("goal", "Find best matching jobs and prepare applications")
    profile = data.get("profile", {})
    provider = data.get("provider", "anthropic")
    llm = LLMClient(provider=provider)
    planner = PlannerAgent(llm)
    return await planner.run(goal, profile)

@router.post("/generate-cover-letter")
async def gen_cover_letter(data: dict):
    job = data.get("job", {})
    profile = data.get("profile", {})
    provider = data.get("provider", "anthropic")
    llm = LLMClient(provider=provider)
    letter = await llm.generate_cover_letter(job, profile)
    return {"cover_letter": letter}

@router.post("/evaluate-offer")
async def evaluate_offer(data: dict):
    offer = data.get("offer", {})
    profile = data.get("profile", {})
    provider = data.get("provider", "anthropic")
    market = {"avg_salary": 165000, "demand": "high", "yoe_multiplier": 1.15}
    llm = LLMClient(provider=provider)
    return await llm.evaluate_offer(offer, market, profile)
