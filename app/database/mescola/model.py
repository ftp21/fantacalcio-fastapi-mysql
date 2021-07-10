from app.database import Base
from app.database.listone.model import Listone
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text,TIMESTAMP
from sqlalchemy.orm import relationship


class Mescola(Base):
    __tablename__ = "mescola"
    id = Column(Integer, primary_key=True)
    ordine = Column(Integer)
    estratto = Column(Integer)
    data_estrazione = Column(TIMESTAMP)
    giocatore = relationship(Listone)
    id_giocatore = Column(ForeignKey('listone.id'), nullable=False)
