from app.database import Base
from sqlalchemy import Column,Integer, String

class Squadre(Base):
    __tablename__ = "squadre"
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))