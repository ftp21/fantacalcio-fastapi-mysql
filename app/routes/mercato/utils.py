from app.routes.rose.utils import get_rosa
from app.routes.configurazione.utils import get_config
from fastapi_sqlalchemy import db
from app.database.listone.model import Listone
from app.database.acquisti.model import Acquisti
def can_i_buy(id_squadra,crediti,id_giocatore):
    giocatore_da_acquistare=db.session.query(Listone).get(id_giocatore)
    config=get_config()
    rosa=get_rosa(id_squadra)
    if giocatore_da_acquistare.ruolo == 'A':
        if rosa.composizione['attaccanti'] >= config.attaccanti:
            return "E' stato raggiunto il limite massimo di attaccanti"
    if giocatore_da_acquistare.ruolo == 'C':
        if rosa.composizione['attaccanti'] >= config.centrocampisti:
            return "E' stato raggiunto il limite massimo di centrocampisti"
    if giocatore_da_acquistare.ruolo == 'D':
        if rosa.composizione['attaccanti'] >= config.difensori:
            return "E' stato raggiunto il limite massimo di difensori"
    if giocatore_da_acquistare.ruolo == 'P':
        if rosa.composizione['portieri'] >= config.portieri:
            return "E' stato raggiunto il limite massimo di Portieri"

    if rosa.crediti_rimanenti-crediti < 0:
        return "Non ci sono abbastanza crediti per effettuare l'acquisto"

    return ""

def svincolatore(id_giocatore):
    config=get_config()
    giocatore_acquisti = db.session.query(Acquisti).filter(Acquisti.id_giocatore == id_giocatore).first()
    giocatore = db.session.query(Listone).get(id_giocatore)
    if config.raggruppa_portieri == 1 and giocatore.ruolo == 'P':
        id_giocatori_squadra = db.session.query(Listone.id).filter(Listone.ruolo == 'P',
                                                                   Listone.squadra == giocatore.squadra).all()
        for id in id_giocatori_squadra:
            db.session.delete(db.session.query(Acquisti).filter(Acquisti.id_giocatore == int(id.id)).one())
            db.session.commit()

        return id_giocatore

    if giocatore_acquisti != None:
        check_acquisti = db.session.query(Acquisti).filter(
            Acquisti.id_giocatore == giocatore_acquisti.id_giocatore).first()
        if check_acquisti != None:
            db.session.delete(check_acquisti)
            db.session.commit()

    return id_giocatore

    return ""