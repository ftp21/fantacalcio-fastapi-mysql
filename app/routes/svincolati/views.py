from fastapi import APIRouter
from app.database.listone.model import Listone
from app.routes.svincolati.schemas.svincolati import Svincolati
from app.database.acquisti.model import Acquisti
from typing import List
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
router = APIRouter(tags=['Visualizzazione Svincolati'])

@router.get('/svincolati',response_model=Svincolati,name='Svincolati')
def get_svincolati() -> Svincolati:
    portieri = db.session.query(Listone).filter(Listone.id.not_in(
            db.session.query(Acquisti.id_giocatore)
        ),Listone.ruolo=='P').all()
    difensori = db.session.query(Listone).filter(Listone.id.not_in(
        db.session.query(Acquisti.id_giocatore)
    ), Listone.ruolo == 'D').all()
    centrocampisti = db.session.query(Listone).filter(Listone.id.not_in(
        db.session.query(Acquisti.id_giocatore)
    ), Listone.ruolo == 'C').all()
    attaccanti = db.session.query(Listone).filter(Listone.id.not_in(
        db.session.query(Acquisti.id_giocatore)
    ), Listone.ruolo == 'A').all()


    return Svincolati(
        portieri=portieri,
        difensori=difensori,
        centrocampisti=centrocampisti,
        attaccanti=attaccanti
    )