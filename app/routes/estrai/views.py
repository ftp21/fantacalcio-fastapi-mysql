from fastapi import APIRouter,Form
from .schemas.estratto import Estratto,Info
from .utils import get_avanti,get_indietro
# from app.database.mescola.model import Mescola
# from typing import List
router = APIRouter(tags=['Estrazione'])


@router.get('/avanti')
def avanti() -> Estratto:
    # estratti = db.session.query(Mescola).filter(Mescola.estratto == 1).count()
    # totali = db.session.query(Mescola).count()
    # rimanenti = int(totali) - int(estratti)



    return get_avanti()


@router.get('/indietro')
def indietro() -> Estratto:
    return get_indietro()