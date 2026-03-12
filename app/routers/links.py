from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.link import LinkCreate, LinkResponse
from app.services import links as service

router = APIRouter(prefix="links", tags="links")

@router.post("/create", response_model=LinkResponse)
def create_shortcut(payload: LinkCreate, db: Session = Depends(get_db)):
    return service.create_link(db, payload)