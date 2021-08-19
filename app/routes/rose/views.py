from fastapi import APIRouter
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from app.database.squadre.model import Squadre
from app.routes.rose.schemas.rosa import Rosa
from .utils import get_rosa
router = APIRouter(tags=['Visualizzazione Rosa'])

@router.get('/rosa/{id_squadra}', response_model=Rosa,name="Rosa",)
def rosa(id_squadra) :
    if db.session.query(Squadre).get(id_squadra):
        return get_rosa(id_squadra)
@router.get('/personal/{otp}',response_model=Rosa,name="Rosa by OTP")
def rosa_by_otp(otp):
    squadra=db.session.query(Squadre).where(Squadre.code==otp).one()
    return get_rosa(squadra.id)