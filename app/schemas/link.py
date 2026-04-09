import datetime
import re

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator, model_validator

SAFE_SLUG_PATTERN = re.compile(r"^[a-z0-9_-]{3,32}$")
RESERVED_SLUGS = {"links", "docs", "openapi.json", "redoc"}

class LinkCreate(BaseModel):
    url: HttpUrl
    slug: str | None = None
    expires_at: datetime.datetime | None = None
    max_uses: int | None = None
    
    @field_validator("slug")
    def validate_slug(cls, value: str | None) -> str | None:
        if value is None:
            return value

        normalized = value.strip().lower()
        if not SAFE_SLUG_PATTERN.fullmatch(normalized):
            raise ValueError(
                "Slug must be 3-32 characters and may only contain lowercase letters, numbers, hyphens, and underscores"
            )
        if normalized in RESERVED_SLUGS:
            raise ValueError("This slug is reserved and cannot be used")
        return normalized

    @model_validator(mode="after")
    def not_both(self) -> "LinkCreate":
        if self.expires_at is not None and self.max_uses is not None:
            raise ValueError("Provide either expires_at or max_uses, not both")
        return self

    @model_validator(mode="after")
    def valid_expiry(self) -> "LinkCreate":
        if self.expires_at is not None and self.expires_at <= datetime.datetime.now(datetime.timezone.utc):
            raise ValueError("Expiration date must be in the future")
        if self.max_uses is not None and self.max_uses <= 0:
            raise ValueError('max_uses must be greater than 0')
        return self

class LinkResponsePublic(BaseModel):
    slug: str
    url: HttpUrl
    created_at: datetime.datetime
    is_active: bool
    click_count: int
    expires_at: datetime.datetime | None = None
    max_clicks: int | None = None

    model_config = ConfigDict(from_attributes=True)

class LinkResponsePrivate(LinkResponsePublic):
    owner_code: str | None = None
    
class LinkStats(BaseModel):
    slug: str
    total_clicks: int
    clicks_by_country: dict[str, int]
    clicks_by_device: dict[str, int]
    last_clicked_at: datetime.datetime | None
