from typing import List, Optional
from pydantic import BaseModel,validator

class Configurazione(BaseModel):

    id : int
    portieri : int
    difensori : int
    centrocampisti : int
    attaccanti : int
    crediti_totali : int
    nascondi_crediti : bool
    raggruppa_portieri : bool

    class Config:
        orm_mode = True

