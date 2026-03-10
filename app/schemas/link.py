from pydantic import BaseModel, HttpUrl
import datetime

class LinkBase(BaseModel):
    url: HttpUrl
    slug: str | None = None

class LinkExpirationDate(LinkBase):
    max_uses: None = None
    expires_at: datetime.datetime | None = None

class LinkMaxUses(LinkBase):
    max_uses: int | None = None
    expires_at: None = None

LinkCreate = LinkMaxUses | LinkExpirationDate

class LinkResponse(BaseModel):
    slug: str
    original_url: str
    short_url: str
    created_at: datetime.datetime
    expires_at: datetime.datetime | None
    max_uses: int | None

    model_config = {"from_attributes": True} 

class LinkStats(BaseModel):
    slug: str
    total_clicks: int
    clicks_by_country: dict[str, int]
    clicks_by_device: dict[str, int]
    last_clicked_at: datetime.datetime | None
