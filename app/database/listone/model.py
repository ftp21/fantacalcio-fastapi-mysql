from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

class Listone(Base):
    __tablename__ = "listone"
    id = Column(Integer, primary_key=True)
    nome_giocatore = Column(String(255))
    squadra = Column(String(255))
    ruolo = Column(String(1))
    campioncino = Column(Text)