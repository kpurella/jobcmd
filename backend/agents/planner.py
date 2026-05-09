"""Planner Agent - orchestrates: Planner → Tools → Memory → Executor loop"""
import asyncio
from typing import List, Dict, Any
from agents.llm_client import LLMClient
from agents.tools import JobScannerTool, MatcherTool, DocumentGeneratorTool, ApplicationTool

class PlannerAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.tools = {
            "scan_jobs": JobScannerTool(),
            "match_jobs": MatcherTool(llm_client),
            "generate_docs": DocumentGeneratorTool(llm_client),
            "apply_job": ApplicationTool(),
        }
        self.memory: List[Dict] = []

    async def run(self, goal: str, profile: Dict) -> Dict[str, Any]:
        self.memory.append({"role": "user", "content": f"Goal: {goal}"})
        plan = self._build_plan(goal, profile)
        results = {}
        for step in plan["steps"]:
            tool_name = step["tool"]
            if tool_name in self.tools:
                result = await self.tools[tool_name].run(step["params"], profile)
                results[step["id"]] = result
                self.memory.append({"role": "tool", "tool": tool_name, "result": str(result)[:200]})
        return {"plan": plan, "results": results, "steps_executed": len(results)}

    def _build_plan(self, goal: str, profile: Dict) -> Dict:
        skills = profile.get("skills", [])[:4]
        return {
            "goal": goal,
            "steps": [
                {"id": "scan", "tool": "scan_jobs",
                 "params": {"keywords": skills},
                 "description": f"Scan 5 job portals for {', '.join(skills[:2])} roles"},
                {"id": "match", "tool": "match_jobs",
                 "params": {"threshold": 0.65},
                 "description": "LLM-score and rank all found jobs against profile"},
                {"id": "docs", "tool": "generate_docs",
                 "params": {"top_n": 3},
                 "description": "Generate tailored cover letters for top 3 matches"},
            ]
        }
