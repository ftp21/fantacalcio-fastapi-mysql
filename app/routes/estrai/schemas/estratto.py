from pydantic import BaseModel,validator,root_validator
from app.routes.configurazione.utils import get_config
class Info(BaseModel):
    rimanenti: int = 0
    estratti: int = 0
    totali: int = 0
class Estratto(BaseModel):
    id: int = ""
    nome_giocatore: str = "Giocatori Finiti"
    squadra: str = ""
    ruolo: str = ""
    ordine: int = ""
    campioncino: str = ""


    @validator('campioncino')
    def raggruppamento(cls,value, values, **kwargs):
        config=get_config()
        if config.raggruppa_portieri==1 and values['ruolo'] =='Portiere':
            values['nome_giocatore'] = ""
            values['campioncino'] = '/stemmi/scudetto.png'
        else:
            values['campioncino'] = value
        return values['campioncino']


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