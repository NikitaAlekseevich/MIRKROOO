from sqlalchemy import Column, String
from database import Base
import uuid

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    photo_url = Column(String, nullable=True)
    privacy_settings = Column(String, default="public")
