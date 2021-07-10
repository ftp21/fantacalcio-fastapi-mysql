from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from fastapi import APIRouter,Form
from sqlalchemy.orm.exc import NoResultFound

from app.database.configurazione.model import Configurazione
from app.routes.configurazione.schemas.default import Configurazione as ConfigurazioneSchema

router = APIRouter(tags=['Gestione Configurazione Generale'])
@router.post('/configurazione')
def set_configurazione(
        portieri: int = Form(...),
        difensori: int = Form(...),
        centrocampisti: int = Form(...),
        attaccanti: int = Form(...),
        raggruppa_portieri: bool = Form(...),
        crediti_totali: int = Form(...),
        crediti_nascosti: bool = Form(...)
):

    db.session.query(Configurazione).delete()
    
    me = Configurazione(
        id=1,
        portieri=portieri,
        difensori=difensori,
        centrocampisti=centrocampisti,
        attaccanti=attaccanti,
        raggruppa_portieri=raggruppa_portieri,
        crediti_totali=crediti_totali,
        nascondi_crediti=crediti_nascosti,
    )
    db.session.add(me)
    db.session.commit()
    return "1"

@router.get('/configurazione')
def get_configurazione() -> ConfigurazioneSchema:
    try:
        return db.session.query(Configurazione).one()
    except NoResultFound:
        return ConfigurazioneSchema(
            id=1,
            portieri=0,
            difensori=0,
            centrocampisti=0,
            attaccanti=0,
            nascondi_crediti=False,
            raggruppa_portieri=False
        )
