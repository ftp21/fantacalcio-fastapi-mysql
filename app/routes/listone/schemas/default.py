from typing import List, Optional
from pydantic import BaseModel,validator
class Listone(BaseModel):
    id : int
    nome_giocatore : str
    squadra : str
    ruolo : str
    campioncino : str

    @validator('ruolo')
    def static_mage(cls, ruolo):
        if ruolo == 'P':
            return 'Portiere'
        if ruolo == 'D':
            return 'Difensore'
        if ruolo == 'C':
            return 'Centrocampista'
        if ruolo == 'A':
            return 'Attaccante'
    class Config:
        orm_mode = True