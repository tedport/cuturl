from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.link import LinkCreate, LinkResponsePublic, LinkStats, LinkResponsePrivate
from app.services import links as service

router = APIRouter(prefix="/links")

@router.post(
    "/",
    response_model=LinkResponsePrivate,
    summary="Create a short link",
    tags=["links"],
    responses={
        400: {"description": "Invalid payload"},
    }
)
def create_shortcut(payload: LinkCreate, db: Session = Depends(get_db)):
    """
    Create a new shortened URL.

    Returns the created link along with a private **owner_code** that can be
    used to manage (e.g. deactivate) the link later.
    """
    link, code = service.create_link(db, payload)
    response = LinkResponsePrivate.model_validate(link)
    response.owner_code = code
    return response


@router.delete(
    "/{slug}",
    status_code=204,
    summary="Deactivate a short link",
    tags=["links"],
    responses={
        204: {"description": "Link successfully deactivated"},
        404: {"description": "Link not found"},
    }
)
def deactivate_shortcut(slug: str, db: Session = Depends(get_db)):
    """
    Deactivate an existing shortened URL by its slug.

    Once deactivated, the link will no longer redirect visitors.
    Requires the **owner_code** returned at creation time.
    """
    return service.deactivate_link(db, slug)


@router.get(
    "/{slug}/stats",
    response_model=LinkStats,
    summary="Get link statistics",
    tags=["links"],
    responses={
        404: {"description": "Link not found"},
    }
)
def stats_shortcut(slug: str, db: Session = Depends(get_db)):
    """
    Retrieve click statistics for a shortened URL.

    Returns aggregated data such as total clicks, unique visitors,
    and user-agent breakdown for the given slug.
    """
    return service.get_link_stats(db, slug)


@router.get(
    "/{slug}",
    response_model=LinkResponsePublic,
    summary="Get link info",
    tags=["links"],
    responses={
        404: {"description": "Link not found"},
    }
)
def info_shortcut(slug: str, db: Session = Depends(get_db)) -> LinkResponsePublic:
    """
    Retrieve public information about a shortened URL by its slug.

    Returns metadata such as the original URL and creation date,
    but does **not** expose the owner code or sensitive stats.
    """
    return service.get_link(db, slug)
