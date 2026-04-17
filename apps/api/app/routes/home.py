from uuid import UUID

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from memory_dropbox.db.session import SessionLocal
from memory_dropbox.repositories.items import get_item, list_items


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    with SessionLocal() as db:
        items = list_items(db, limit=10)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "Memory Dropbox", "items": items},
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

