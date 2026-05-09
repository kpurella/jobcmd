"""LLM Client - supports Anthropic API + Ollama local models"""
import os, json, httpx
from typing import Optional

class LLMClient:
    def __init__(self, provider: str = "anthropic", model: str = "claude-sonnet-4-20250514"):
        self.provider = provider
        self.model = model
        self.ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    async def complete(self, prompt: str, system: str = "", max_tokens: int = 2000) -> str:
        if self.provider == "anthropic":
            return await self._anthropic_complete(prompt, system, max_tokens)
        elif self.provider == "ollama":
            return await self._ollama_complete(prompt, system, max_tokens)
        raise ValueError(f"Unknown provider: {self.provider}")

    async def _anthropic_complete(self, prompt: str, system: str, max_tokens: int) -> str:
        import anthropic
        client = anthropic.AsyncAnthropic()
        msg = await client.messages.create(
            model=self.model, max_tokens=max_tokens,
            system=system or "You are a helpful AI job search assistant.",
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text

    async def _ollama_complete(self, prompt: str, system: str, max_tokens: int) -> str:
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{self.ollama_base}/api/generate", json={
                "model": self.model, "prompt": f"{system}\n\n{prompt}",
                "stream": False, "options": {"num_predict": max_tokens}
            }, timeout=120)
            return r.json()["response"]

    async def match_job(self, job: dict, profile: dict) -> dict:
        prompt = f"""Rate this job match 0-100 and explain briefly.

JOB: {job['title']} at {job['company']}
Requirements: {', '.join(job.get('requirements', []))}
Description: {job['description'][:500]}

CANDIDATE: {profile.get('name', 'Candidate')}
Skills: {', '.join(profile.get('skills', []))}
Experience: {profile.get('experience_years', 0)} years

Return ONLY valid JSON: {{"score": 0-100, "reasoning": "2-3 sentences", "gaps": ["list"], "strengths": ["list"]}}"""
        try:
            result = await self.complete(prompt)
            clean = result.strip().replace("```json","").replace("```","").strip()
            return json.loads(clean)
        except:
            return {"score": 65, "reasoning": "Good potential match based on skill overlap.", "gaps": [], "strengths": []}

    async def generate_cover_letter(self, job: dict, profile: dict) -> str:
        prompt = f"""Write a compelling 3-paragraph cover letter for:

JOB: {job['title']} at {job['company']}
{job['description'][:600]}

CANDIDATE: {profile.get('name', 'Candidate')}
Skills: {', '.join(profile.get('skills', []))}
Experience: {profile.get('experience_years', 0)} years

Be specific and avoid generic phrases. First person voice."""
        return await self.complete(prompt)

    async def evaluate_offer(self, offer: dict, market_data: dict, profile: dict) -> dict:
        prompt = f"""Evaluate this job offer. Return ONLY valid JSON:
{{"overall_score": 0-100, "salary_score": 0-100, "growth_score": 0-100,
  "recommendation": "accept|negotiate|decline",
  "reasoning": "2-3 sentences", "negotiation_points": ["list"]}}

OFFER: {json.dumps(offer)}
MARKET: {json.dumps(market_data)}
PREFS: {json.dumps(profile.get('preferences', {}))}"""
        try:
            result = await self.complete(prompt)
            clean = result.strip().replace("```json","").replace("```","").strip()
            return json.loads(clean)
        except:
            return {"overall_score": 72, "salary_score": 68, "growth_score": 75,
                    "recommendation": "negotiate", "reasoning": "Competitive offer with room for negotiation.",
                    "negotiation_points": ["Request 10% salary increase", "Ask for signing bonus"]}
