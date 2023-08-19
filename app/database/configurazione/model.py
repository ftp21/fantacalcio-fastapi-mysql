from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

class Configurazione(Base):
    __tablename__ = "configurazione"
    id = Column(Integer, primary_key=True)
    portieri = Column(Integer)
    difensori = Column(Integer)
    centrocampisti = Column(Integer)
    attaccanti = Column(Integer)
    crediti_totali = Column(Integer)
    nascondi_crediti = Column(Boolean)
    raggruppa_portieri = Column(Boolean)
    offerta_minima = Column(Integer)
