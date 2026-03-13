from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.link import LinkCreate, LinkResponse, LinkStats
from app.services import links as service

router = APIRouter(prefix="links")

@router.post("/", response_model=LinkResponse)
def create_shortcut(payload: LinkCreate, db: Session = Depends(get_db)):
    return service.create_link(db, payload)
@router.delete('/{slug}', status_code=204)
def deactivate_shortcut(slug: str, db: Session = Depends(get_db)):
    return service.deactivate_link(db, slug)
@router.get('/{slug}/stats', response_model=LinkStats)
def stats_shortcut(slug: str, db: Session = Depends(get_db)):
    return service.get_link_stats(db, slug)
@router.get('/{slug}', response_model=LinkResponse)
def info_shortcut(slug: str, db: Session = Depends(get_db)) -> LinkResponse:
    return service.get_link(db, slug)