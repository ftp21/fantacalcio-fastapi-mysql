from pydantic import BaseModel,validator
from app.routes.mescola.schemas.parametri import Parametri
from app.routes.rose.schemas.giocatore import GiocatoreAcquistato
from app.routes.estrai.schemas.estratto import Estratto
class Info(BaseModel):
    rimanenti: int = 0
    estratti: int = 0
    totali: int = 0
class Status(BaseModel):
    mescola: Parametri or []
    ultimo_acquisto: GiocatoreAcquistato or []
    estratto: Estratto
    info: Info



    class Config:
        orm_mode = True
        validate_assignment = True