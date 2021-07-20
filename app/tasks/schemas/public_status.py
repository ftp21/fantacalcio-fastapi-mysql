from pydantic import BaseModel,validator,root_validator
from app.routes.configurazione.utils import get_config
from typing import List,Dict,Optional
import os
from app.routes.mescola.schemas.parametri import Parametri
from app.routes.rose.schemas.giocatore import GiocatoreAcquistato
from app.routes.estrai.schemas.estratto import Estratto
class Info(BaseModel):
    rimanenti: int = 0
    estratti: int = 0
    totali: int = 0
class Estratto_public(BaseModel):
    id: int = ""
    nome_giocatore: str = "Giocatori Finiti"
    squadra: str = ""
    ruolo: str = ""
    ordine: int = ""
    campioncino: str = ""

    @validator('campioncino')
    def raggruppamento(cls, value, values, **kwargs):
        config = get_config()
        if config.raggruppa_portieri == 1 and values['ruolo'] == 'Portiere':
            values['nome_giocatore'] = values['squadra']
            values['squadra']=""
            if os.path.exists('/home/fastapi/stemmi/' + values['squadra'] + '.png'):
                values['campioncino'] = '/stemmi/' + values['squadra'] + '.png'
            else:
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
class Acquisto_public(BaseModel):
    id_fanta_squadra: int = ""
    fanta_squadra: str = ""
    crediti: int = ""
    id_giocatore: int = ""
    nome_giocatore: str = ""
    squadra: str = ""
    ruolo: str = ""
    campioncino: str = ""

    @validator('crediti')
    def hide_rimanenti(cls, crediti_):
        config = get_config()
        if config.nascondi_crediti == True:
            return ""
        else:
            return crediti_
    # @validator('campioncino')
    # def raggruppamento(cls, value, values, **kwargs):
    #     config = get_config()
    #     if config.raggruppa_portieri == 1 and values['ruolo'] == 'Portiere':
    #         values['nome_giocatore'] = values['squadra']
    #         if os.path.exists('../stemmi/' + values['squadra'] + '.png'):
    #             values['campioncino'] = '/stemmi/' + values['squadra'] + '.png'
    #         else:
    #             values['campioncino'] = '/stemmi/scudetto.png'
    #     else:
    #         values['campioncino'] = value
    #     return values['campioncino']

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
class Rose_public(BaseModel):
    id: int =0
    nome: str = 0
    composizione: Dict = {}
    crediti_rimanenti: int = 0
    crediti_spesi: int = 0

    @validator('crediti_rimanenti')
    def hide_rimanenti(cls, crediti_rimanenti):
        config=get_config()
        if config.nascondi_crediti == True:
            return ""
        else:
            return crediti_rimanenti

    @validator('crediti_spesi')
    def hide_spesi(cls, crediti_spesi):
        config = get_config()
        if config.nascondi_crediti == True:
            return ""
        else:
            return crediti_spesi

class Public_state(BaseModel):
    estratto: Estratto_public
    ultimo_acquisto: Acquisto_public
    rose: Optional[List[Rose_public]]
    info: Info