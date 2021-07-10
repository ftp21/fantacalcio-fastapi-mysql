from app.routes.listone.schemas.default import Listone
from pydantic import BaseModel,validator
from typing import List
class Svincolati(BaseModel):
    portieri: List[Listone]
    difensori: List[Listone]
    centrocampisti: List[Listone]
    attaccanti: List[Listone]
    class Config:
        orm_mode = True