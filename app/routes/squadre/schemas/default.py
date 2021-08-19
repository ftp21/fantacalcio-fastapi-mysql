from pydantic import BaseModel,validator
class Squadre(BaseModel):
    id : int
    nome : str
    code: str
    class Config:
        orm_mode = True