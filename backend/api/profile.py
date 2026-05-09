from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional
import json, os

router = APIRouter()
PROFILE_FILE = "./data/profile.json"

class ProfileModel(BaseModel):
    name: str
    email: str
    skills: List[str]
    experience_years: int
    resume_text: Optional[str] = ""
    preferences: Optional[Dict] = {}

@router.get("/")
async def get_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE) as f: return json.load(f)
    return {}

@router.post("/")
async def save_profile(profile: ProfileModel):
    os.makedirs("./data", exist_ok=True)
    with open(PROFILE_FILE, "w") as f: json.dump(profile.dict(), f, indent=2)
    return {"status": "saved", "profile": profile.dict()}
