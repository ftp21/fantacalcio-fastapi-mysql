from fastapi import APIRouter,Depends,Request,BackgroundTasks
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from app.routes.mescola.utils import revese_mescola
from app.database.mescola.model import Mescola
from app.database.acquisti.model import Acquisti
from app.database.listone.model import Listone
from app.database.squadre.model import Squadre
from app.routes.estrai.schemas.estratto import Estratto
from .schemas.status import Status as StatusSchema,Info
from app.tasks.push_update import push_update
router = APIRouter(tags=["Get status attuale"])

@router.get('/status')
async def get_status(request: Request,background_tasks: BackgroundTasks) -> StatusSchema:
    mescola=revese_mescola()
    ultimo_acquisto=db.session.query(Squadre.nome.label('fanta_squadra'),
                              Listone.nome_giocatore,
                              Listone.squadra,
                              Listone.ruolo,
                              Listone.campioncino,
                              Acquisti.crediti,Acquisti).join(Listone,Listone.id==Acquisti.id_giocatore).join(Squadre,Squadre.id==Acquisti.id_squadra).order_by(Acquisti.ora.desc()).first() or []

    estratto=db.session.query(Listone.id,
                              Listone.nome_giocatore,
                              Listone.squadra,
                              Listone.ruolo,
                              Listone.campioncino,
                              Mescola.ordine).join(Listone,Listone.id==Mescola.id_giocatore).where(Mescola.estratto!=None).order_by(Mescola.ordine.desc()).first()
    estratti=db.session.query(Mescola).filter(Mescola.estratto==1).count()
    totali=db.session.query(Mescola).count()
    rimanenti=int(totali)-int(estratti)
    totale_listone=db.session.query(Listone).count()
    if estratto == None:
        estratto=Estratto(
            id=0,
            nome_giocatore="Inizia ad estrarre"
        )
    db.session.commit()
    background_tasks.add_task(push_update)
    # requests.get(trigger)
    return StatusSchema(
        mescola=mescola,
        ultimo_acquisto=ultimo_acquisto,
        estratto=estratto,
        info=Info(
            estratti=estratti,
            totali=totali,
            rimanenti=rimanenti
        ),
        totale_listone=totale_listone
    )