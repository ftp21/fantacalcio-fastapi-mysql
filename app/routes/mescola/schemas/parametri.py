from pydantic import BaseModel
class Parametri(BaseModel):
    portieri: bool
    difensori: bool
    centrocampisti: bool
    attaccanti: bool
    alfabetico: bool
