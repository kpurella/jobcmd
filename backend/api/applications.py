from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import json, os, datetime, uuid

router = APIRouter()
APPS_FILE = "./data/applications.json"

def load_apps():
    if os.path.exists(APPS_FILE):
        with open(APPS_FILE) as f: return json.load(f)
    return []

def save_apps(apps):
    os.makedirs("./data", exist_ok=True)
    with open(APPS_FILE, "w") as f: json.dump(apps, f, indent=2, default=str)

class ApplicationModel(BaseModel):
    job_id: str
    job_title: str
    company: str
    cover_letter: Optional[str] = ""
    status: Optional[str] = "applied"
    salary_offered: Optional[float] = None
    notes: Optional[str] = ""

@router.get("/")
async def list_applications():
    return {"applications": load_apps()}

@router.post("/")
async def create_application(app: ApplicationModel):
    apps = load_apps()
    new_app = app.dict()
    new_app["id"] = uuid.uuid4().hex[:8]
    new_app["applied_at"] = datetime.datetime.utcnow().isoformat()
    new_app["updated_at"] = new_app["applied_at"]
    apps.append(new_app)
    save_apps(apps)
    return {"status": "created", "application": new_app}

@router.patch("/{app_id}")
async def update_application(app_id: str, data: dict):
    apps = load_apps()
    for app in apps:
        if app["id"] == app_id:
            app.update(data)
            app["updated_at"] = datetime.datetime.utcnow().isoformat()
    save_apps(apps)
    return {"status": "updated"}

@router.delete("/{app_id}")
async def delete_application(app_id: str):
    save_apps([a for a in load_apps() if a["id"] != app_id])
    return {"status": "deleted"}
