from pydantic import BaseModel,validator
class Squadre(BaseModel):
    id : int
    nome : str
    class Config:
        orm_mode = True