from sqlalchemy import Column, Integer, LargeBinary, String, Boolean

from common import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, index=True)
    filename = Column(String)
    content_type = Column(String)
    data = Column(LargeBinary)
    converted = Column(Boolean)
