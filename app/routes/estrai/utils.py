from app.database.mescola.model import Mescola
from app.database.listone.model import Listone
from sqlalchemy import and_,text,desc

from .schemas.estratto import Estratto
from fastapi_sqlalchemy import db  # an object to provide global access to a database session


def get_avanti() -> Estratto:
    me = Estratto()
    # Query Next Estratto
    #     SELECT * FROM listone where estratto is NULL and ordine is not null order by ordine limit 1
    estratto = db.session.query(Mescola).join(Listone).filter(
        and_(Mescola.estratto == None, Mescola.ordine != None)).order_by(Mescola.ordine).limit(
        1).first()
    if estratto is not None:
        estratto.estratto = 1
        estratto.data_estrazione = text("now()")
        db.session.commit()
        return Estratto(
            id=estratto.giocatore.id,
            nome_giocatore=estratto.giocatore.nome_giocatore,
            squadra = estratto.giocatore.squadra,
            ruolo = estratto.giocatore.ruolo,
            campioncino = estratto.giocatore.campioncino,
            ordine = estratto.ordine
        )

    else:
        return Estratto()


def get_indietro() -> Estratto:
    estratto = db.session.query(Mescola).join(Listone).filter(and_(Mescola.estratto != None, Mescola.ordine != None)).order_by(
        desc(
            Mescola.ordine)).limit(3).all()
    if estratto is not None:
        # Se sono usciti più di un giocatore logicamente mi trovero' almeno 2 record
        if len(estratto) > 1:
            estratto[0].estratto = None
            estratto[0].data_estrazione= None
            db.session.commit()
            return Estratto(
                id=estratto[1].giocatore.id,
                nome_giocatore=estratto[1].giocatore.nome_giocatore,
                squadra=estratto[1].giocatore.squadra,
                ruolo=estratto[1].giocatore.ruolo,
                campioncino=estratto[1].giocatore.campioncino,
                ordine=estratto[1].ordine
            )


        elif len(estratto) == 1:
            return Estratto(
                id=estratto[0].giocatore.id,
                nome_giocatore=estratto[0].giocatore.nome_giocatore,
                squadra=estratto[0].giocatore.squadra,
                ruolo=estratto[0].giocatore.ruolo,
                campioncino=estratto[0].giocatore.campioncino,
                ordine=estratto[0].ordine
            )

    return Estratto()
