import app
from app.routes.squadre.views import get_squadre
from fastapi import Request
from app.routes.rose.utils import get_rosa
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from app.database.mescola.model import Mescola

from app.database.acquisti.model import Acquisti
from app.database.listone.model import Listone
from app.database.squadre.model import Squadre
from .schemas.public_status import Public_state,Info,Rose_public

async def push_update():
    squadre=get_squadre()
    public=[]
    for s in squadre:
        rosa=get_rosa(s.id)

        public.append(
            Rose_public(
                id=s.id,
                nome=s.nome,
                composizione= rosa.composizione,
                crediti_rimanenti=rosa.crediti_rimanenti,
                crediti_spesi=rosa.crediti_spesi
            )
        )

    ultimo_acquisto = db.session.query(Squadre.nome.label('fanta_squadra'),
                                       Listone.nome_giocatore,
                                       Listone.squadra,
                                       Listone.ruolo,
                                       Listone.campioncino,
                                       Acquisti.crediti, Acquisti).join(Listone,
                                                                        Listone.id == Acquisti.id_giocatore).join(
        Squadre, Squadre.id == Acquisti.id_squadra).order_by(Acquisti.ora.desc()).first() or []

    estratto = db.session.query(Listone.id,
                                Listone.nome_giocatore,
                                Listone.squadra,
                                Listone.ruolo,
                                Listone.campioncino,
                                Mescola.ordine).join(Listone, Listone.id == Mescola.id_giocatore).where(
        Mescola.estratto != None).order_by(Mescola.ordine.desc()).first()
    estratti = db.session.query(Mescola).filter(Mescola.estratto == 1).count()
    totali = db.session.query(Mescola).count()
    rimanenti = int(totali) - int(estratti)




    await app.manager.broadcast(
        Public_state(
            estratto=estratto,
            ultimo_acquisto=ultimo_acquisto,
            rose=public,
            info=Info(
                estratti=estratti,
                totali=totali,
                rimanenti=rimanenti
            )
        ).json()
    )
    return ""