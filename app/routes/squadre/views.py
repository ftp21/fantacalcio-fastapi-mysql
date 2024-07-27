from fastapi import APIRouter,Form
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from app.database.squadre.model import Squadre
from app.database.acquisti.model import Acquisti
from .schemas.default import Squadre as SquadreSchema
from typing import List
from random import randint

router = APIRouter(tags=["Gestione Squadre"])

@router.get('/squadre')
def get_squadre() -> List[SquadreSchema]:
    return db.session.query(Squadre).all()

@router.post('/squadre')
def add_squadre(
        nome: str = Form(...)
    ) -> str:
    db.session.add(
        Squadre(
            nome=nome,
            code=''.join(["{}".format(randint(0, 9)) for num in range(0, 5)])
        )
    )
    db.session.commit()
    return nome

@router.put('/squadre/{id_squadra}')
def rename_squadre(
        id_squadra: int,
        nome:str = Form(...)
    )-> str:

    squadra=db.session.query(Squadre).get(id_squadra)
    squadra.nome=nome
    db.session.commit()
    return nome

@router.delete('/squadre/{id_squadra}')
def delete_squadra(
        id_squadra: int,
    ) -> str:

    rosa=db.session.query(Acquisti).filter(Acquisti.id_squadra==id_squadra)
    for r in rosa:
        db.session.delete(r)
    db.session.commit()

    db.session.delete(
        db.session.query(Squadre).get(id_squadra)
    )
    db.session.commit()
    return id_squadra