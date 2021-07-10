from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from app.database.configurazione.model import Configurazione
from .schemas.default import Configurazione as ConfigurazioneSchema

def get_config() -> ConfigurazioneSchema:
    return db.session.query(Configurazione).one()
