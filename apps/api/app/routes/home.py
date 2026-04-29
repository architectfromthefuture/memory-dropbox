from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from memory_dropbox.db.session import SessionLocal
from memory_dropbox.events import get_recent_memory_activity
from memory_dropbox.repositories.items import get_item, list_items


router = APIRouter()
_API_ROOT = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(_API_ROOT / "templates"))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    with SessionLocal() as db:
        items = list_items(db, limit=10)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "Memory Dropbox", "items": items},
    )


@router.get("/ui/memory", response_class=HTMLResponse)
async def memory_activity_page(request: Request):
    activity = get_recent_memory_activity(limit=100)
    return templates.TemplateResponse(
        request=request,
        name="memory_activity.html",
        context={"title": "Memory Activity", "activity": activity},
    )


@router.get("/ui/items/{item_id}", response_class=HTMLResponse)
async def item_detail(request: Request, item_id: UUID):
    with SessionLocal() as db:
        item = get_item(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse(
        request=request,
        name="item_detail.html",
        context={"title": f"Item {item_id}", "item": item},
    )
