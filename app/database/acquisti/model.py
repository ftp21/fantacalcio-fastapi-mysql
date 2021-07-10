from app.database import Base
from app.database.listone.model import Listone
from app.database.squadre.model import Squadre
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text,TIMESTAMP
from sqlalchemy.orm import relationship



class Acquisti(Base):
    __tablename__ = "acquisti"
    id = Column(Integer, primary_key=True)
    crediti = Column(Integer)
    ora = Column(TIMESTAMP)

    squadra = relationship(Squadre)
    id_squadra = Column(ForeignKey('squadre.id'), nullable=False)
    giocatore = relationship(Listone)
    id_giocatore = Column(ForeignKey('listone.id'), nullable=False)