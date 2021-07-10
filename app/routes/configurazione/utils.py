from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from app.database.configurazione.model import Configurazione
from .schemas.default import Configurazione as ConfigurazioneSchema
from sqlalchemy.orm.exc import NoResultFound


def get_config() -> ConfigurazioneSchema:
    try:
        config=db.session.query(Configurazione).one()
    except NoResultFound:
        config= ConfigurazioneSchema(
            id=1,
            portieri=0,
            difensori=0,
            centrocampisti=0,
            attaccanti=0,
            nascondi_crediti=False,
            raggruppa_portieri=False
        )
    return config