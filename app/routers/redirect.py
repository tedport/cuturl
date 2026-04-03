from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services import redirect as service

router = APIRouter()

def cuturl_redirect(slug: str, request: Request, db: Session = Depends(get_db)):
    """
    Redirect the client to the original URL associated with the given slug.

    Also records the click, capturing the visitor's **IP address** and
    **User-Agent** for analytics purposes.
    """
    return service.get_link_and_register_click(
        db, slug, request.client.host, request.headers.get("User-Agent")
    ).url