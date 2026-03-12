from sqlalchemy import IntegrityError, select
from sqlalchemy.orm import Session
from app.core.exceptions import LinkNotFoundError, SlugGenerationError, SlugTakenError
from app.models.link import Link
from app.schemas.link import LinkCreate
import nanoid

def get_link(db: Session, slug: str) -> Link:
    link = db.scalars(select(Link).where(Link.slug == slug)).one_or_none()
    if not link:
        raise LinkNotFoundError(f"Slug '{slug}' doesn't exist")
    return link

def create_link(db: Session, payload: LinkCreate) -> Link:
    for _ in range(15):
        slug = payload.slug or nanoid.generate(size=8)

        link = Link(
            slug=slug,
            url=str(payload.url),
            expires_at=payload.expires_at,
            max_clicks=payload.max_uses,
        )
        db.add(link)
        try:
            db.commit()
            db.refresh(link)
            return link
        except IntegrityError:
            db.rollback()
            if payload.slug:
                raise SlugTakenError(f"Slug '{slug}' is already taken")
            continue

    raise SlugGenerationError("Could not generate a unique slug, try again")