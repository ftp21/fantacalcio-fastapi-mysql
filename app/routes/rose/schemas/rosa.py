from pydantic import BaseModel,validator
from .giocatore import GiocatoreAcquistato
from typing import List,Dict
class Rosa(BaseModel):
    nome_squadra: str
    portieri: List[GiocatoreAcquistato] = []
    difensori: List[GiocatoreAcquistato] = []
    centrocampisti: List[GiocatoreAcquistato] = []
    attaccanti: List[GiocatoreAcquistato] = []
    crediti_rimanenti: int = 0
    crediti_spesi: int = 0
    composizione: Dict = {}