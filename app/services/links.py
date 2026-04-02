import nanoid
import datetime
import pickle

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from typing import Optional

from app.core.exceptions import LinkExpiredError, LinkInactiveError, LinkNotFoundError, SlugGenerationError, SlugTakenError, LinkAccessDeniedError
from app.core.security import verify_password, get_password_hash
from app.models import Click, Link
from app.schemas.link import LinkCreate, LinkStats

def get_link(db: Session, slug: str):
    link = db.scalars(select(Link).where(Link.slug == slug)).one_or_none()
    if not link:
        raise LinkNotFoundError()
    if not link.is_active:
        raise LinkInactiveError()
    if (link.expires_at and link.expires_at < datetime.datetime.now(datetime.timezone.utc)) or\
        (link.max_clicks and link.click_count > link.max_clicks):
        raise LinkExpiredError()
    return link

def deactivate_link(db: Session, slug: str, code: str):
    link = db.scalars(select(Link).where(Link.slug == slug)).one_or_none()
    if not link:
        raise LinkNotFoundError()
    if not verify_password(code, link.hashed_code):
        raise LinkAccessDeniedError()
    if db.execute(update(Link)
               .where(Link.slug == slug)
               .values(is_active=False)).rowcount <= 0:
        raise LinkNotFoundError()
    db.commit()

def create_link(db: Session, payload: LinkCreate) -> tuple[Link, str]:
    for _ in range(15):
        slug = payload.slug or nanoid.generate(size=8)
        code = nanoid.generate(size=12)

        link = Link(
            slug=slug,
            url=str(payload.url),
            expires_at=payload.expires_at,
            max_clicks=payload.max_uses,
            hashed_code = get_password_hash(code)
        )
        db.add(link)
        try:
            db.commit()
            db.refresh(link)
            return (link, code)
        except IntegrityError:
            db.rollback()
            if payload.slug:
                raise SlugTakenError(f"Slug '{slug}' is already taken")
            continue

    raise SlugGenerationError("Could not generate a unique slug, try again")

from collections import Counter

def get_link_stats(db: Session, slug: str) -> LinkStats:
    link = db.scalars(select(Link).where(Link.slug == slug)).one_or_none()

    if not link:
        raise LinkNotFoundError()

    clicks = db.query(Click).filter(Click.link_id == link.id).all()

    clicks_by_country = Counter(
        c.country or "Unknown" for c in clicks
    )
    clicks_by_device = Counter(
        c.device or "Unknown" for c in clicks
    )
    last_clicked_at = max(
        (c.timestamp for c in clicks),
        default=None
    )

    return LinkStats(
        slug=slug,
        total_clicks=link.click_count,
        clicks_by_country=dict(clicks_by_country),
        clicks_by_device=dict(clicks_by_device),
        last_clicked_at=last_clicked_at,
    )