import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    url = Column(String, nullable=False)
    hashed_code = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True)
    click_count = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)
    max_clicks = Column(Integer, nullable=True)
    
    clicks = relationship("Click", back_populates="link")