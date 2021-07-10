from .schemas.parametri import Parametri
from app.database.listone.model import Listone
from app.database.mescola.model import Mescola
from app.routes.configurazione.utils import get_config
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
import random

def parse_and_scramble(parametri: Parametri):
    clausole = []
    if parametri.portieri:
        clausole.append('P')
    if parametri.difensori:
        clausole.append('D')
    if parametri.centrocampisti:
        clausole.append('C')
    if parametri.attaccanti:
        clausole.append('A')


    config_generale=get_config()

    portieri_raggruppati = []
    if config_generale.raggruppa_portieri and 'P' in clausole:
        # QUI RAGGRUPPO LE SQUADRE MA SOLO PER I PORTIERI
        if parametri.alfabetico:
            portieri_raggruppati = db.session.query(Listone).filter(Listone.ruolo == 'P').group_by(
                Listone.squadra).order_by(Listone.squadra).all()
        else:
            portieri_raggruppati = db.session.query(Listone).filter(Listone.ruolo == 'P').group_by(
                Listone.squadra).all()
            random.shuffle(portieri_raggruppati)
        clausole.remove('P')
    if parametri.alfabetico:
        giocatori = db.session.query(Listone).filter(Listone.ruolo.in_(clausole)).order_by(
            Listone.nome_giocatore).all()
    else:
        giocatori = db.session.query(Listone).filter(Listone.ruolo.in_(clausole)).all()
    if len(portieri_raggruppati) > 0:
        if parametri.alfabetico == False:
            random.shuffle(giocatori)
        giocatori = portieri_raggruppati + giocatori
    else:
        if parametri.alfabetico == False:
            random.shuffle(giocatori)
    index = 0
    db.session.query(Mescola).delete()
    db.session.commit()
    for giocatore in giocatori:
        index += 1
        db.session.add(
            Mescola(
                id_giocatore=giocatore.id,
                ordine=index
            )
        )

    db.session.commit()
    primo=db.session.query(Mescola).filter(Mescola.ordine==1).one()
    primo.estratto=1
    db.session.commit()
    return len(giocatori)


def revese_mescola() -> Parametri:
    r = db.session.query(Mescola).join(Listone).group_by(Listone.ruolo).all()
    ruoli = []
    for ru in r:
        ruoli.append(ru.giocatore.ruolo)

    ''' check alfabetico '''
    config_generale = get_config()
    if config_generale.raggruppa_portieri == 1 and 'P' in ruoli:
        ordered = db.session.query(Mescola).join(Listone,Listone.id==Mescola.id_giocatore).order_by(Listone.squadra).all()
    else:
        ordered = db.session.query(Mescola).join(Listone, Listone.id == Mescola.id_giocatore).order_by(
            Listone.nome_giocatore).all()
    not_ordered = db.session.query(Mescola).join(Listone).order_by(Mescola.ordine).all()
    alfabetico = False

    for o, no in zip(ordered, not_ordered):
        if o.giocatore.id == no.giocatore.id:
            alfabetico = True
        else:
            alfabetico = False
            break

    ret=Parametri(
        portieri = False,
        difensori = False,
        centrocampisti = False,
        attaccanti = False,
        alfabetico = alfabetico
    )

    if 'P' in ruoli:
        ret.portieri = True
    if 'D' in ruoli:
        ret.difensori = True
    if 'C' in ruoli:
        ret.centrocampisti = True
    if 'A' in ruoli:
        ret.attaccanti = True

    return ret
