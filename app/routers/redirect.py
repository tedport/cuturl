from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services import redirect as service

router = APIRouter()

@router.get("/{slug}", response_class=RedirectResponse, status_code=302)
def cuturl_redirect(slug : str, request : Request, db: Session = Depends(get_db)):
    return service.get_link_and_register_click(db, slug, request.client.host, request.headers.get("User-Agent")).url