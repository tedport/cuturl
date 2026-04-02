import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl, computed_field, model_validator

from app.core.config import settings

class LinkCreate(BaseModel):
    url: HttpUrl
    slug: str | None = None
    expires_at: datetime.datetime | None = None
    max_uses: int | None = None
    
    @model_validator(mode="after")
    def not_both(self) -> "LinkCreate":
        if self.expires_at is not None and self.max_uses is not None:
            raise ValueError("Provide either expires_at or max_uses, not both")
        return self

class LinkResponsePublic(BaseModel):
    slug: str
    url: HttpUrl
    created_at: datetime.datetime
    is_active: bool
    click_count: int
    expires_at: datetime.datetime | None = None
    max_clicks: int | None = None
    
    @computed_field
    @property
    def short_url(self) -> str:
        return f"{settings.BASE_URL}/{self.slug}"

    model_config = ConfigDict(from_attributes=True)

class LinkResponsePrivate(LinkResponsePublic):
    owner_code: str | None = None
    
class LinkStats(BaseModel):
    slug: str
    total_clicks: int
    clicks_by_country: dict[str, int]
    clicks_by_device: dict[str, int]
    last_clicked_at: datetime.datetime | None
