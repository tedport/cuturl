from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import *

class Click(Base):
    __tablename__ = "clicks"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    link_id = Column(Integer, ForeignKey('links.id'), nullable=False)
    country = Column(String, nullable=True)
    device = Column(String, nullable=True)
    
    link = relationship("Link", back_populates="clicks")