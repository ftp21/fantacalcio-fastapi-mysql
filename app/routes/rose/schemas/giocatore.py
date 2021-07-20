from pydantic import BaseModel,validator
from app.routes.configurazione.utils import get_config
import os.path

class GiocatoreAcquistato(BaseModel):
    id_fanta_squadra: int = ""
    fanta_squadra: str = ""
    crediti: int = ""
    id_giocatore: int = ""
    nome_giocatore : str = ""
    squadra: str = ""
    ruolo : str = ""
    campioncino : str = ""

    @validator('campioncino')
    def raggruppamento(cls, value, values, **kwargs):
        config = get_config()
        if config.raggruppa_portieri == 1 and values['ruolo'] == 'Portiere':
            values['nome_giocatore'] = values['squadra']
            if os.path.exists('stemmi/'+values['squadra']+'.png'):
                values['campioncino'] = '/stemmi/'+values['squadra']+'.png'
            else:
                values['campioncino'] = '/stemmi/scudetto.png'
        else:
            values['campioncino'] = value

        if values['campioncino']=="":
            values['campioncino'] = '/stemmi/scudetto.png'
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