from sqlalchemy import Column, Integer, String, Text
from database import Base

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(Text)
