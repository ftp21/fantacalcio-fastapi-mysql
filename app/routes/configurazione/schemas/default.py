from typing import List, Optional
from pydantic import BaseModel,validator

class Configurazione(BaseModel):

    id : int
    portieri : int = 0
    difensori : int = 0
    centrocampisti : int = 0
    attaccanti : int = 0
    crediti_totali : int = 0
    nascondi_crediti : bool = False
    raggruppa_portieri : bool = False

    class Config:
        orm_mode = True

