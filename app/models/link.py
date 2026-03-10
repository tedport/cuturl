from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import *

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    click_count = Column(Integer, default=0)
    
    clicks = relationship("Click", back_populates="clicks")