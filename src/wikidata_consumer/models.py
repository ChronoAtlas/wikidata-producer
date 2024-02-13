from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Point(Base):
    __tablename__ = "locations"
    event_id = Column(String, nullable=False, primary_key=True)
    point = Column(String, nullable=False)
