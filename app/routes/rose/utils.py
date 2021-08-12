from app.database.acquisti.model import Acquisti
from app.database.listone.model import Listone
from app.database.squadre.model import Squadre
from app.routes.configurazione.utils import get_config
from .schemas.rosa import Rosa
from sqlalchemy.sql import func

from fastapi_sqlalchemy import db


def get_rosa(id_squadra,export=0) -> Rosa:
    config=get_config()
    #SELECT * FROM fantacalcio.acquisti inner join fantacalcio.listone on listone.id=acquisti.id_giocatore inner join fantacalcio.squadre on acquisti.id_squadra=squadre.id where id_squadra=2;
    portieri=_get_rosa_ruolo('P',id_squadra,export)
    difensori = _get_rosa_ruolo('D',id_squadra,export)
    centrocampisti = _get_rosa_ruolo('C',id_squadra,export)
    attaccanti = _get_rosa_ruolo('A',id_squadra,export)

    crediti_spesi=db.session.query(func.sum(Acquisti.crediti).label('crediti_spesi')).filter(Acquisti.id_squadra==id_squadra).first()


    composizione={
        'portieri' :len(portieri),
        'difensori':len(difensori),
        'centrocampisti': len(centrocampisti),
        'attaccanti': len(attaccanti)
    }
    # if config.raggruppa_portieri == 1:
    #     num_portieri = db.session.query(Acquisti).join(Listone, Listone.id == Acquisti.id_giocatore).join(Squadre,Squadre.id == Acquisti.id_squadra).where(Acquisti.id_squadra == id_squadra, Listone.ruolo == 'P').group_by(Listone.squadra).all()
    #     composizione['portieri'] = len(num_portieri)
    # else:
    #     composizione['portieri']=len(portieri)


    return Rosa(
        portieri=portieri,
        difensori=difensori,
        centrocampisti=centrocampisti,
        attaccanti=attaccanti,
        crediti_spesi=int(crediti_spesi.crediti_spesi or 0),
        crediti_rimanenti=int(config.crediti_totali or 0)-int(crediti_spesi.crediti_spesi or 0),
        composizione=composizione
    )


def _get_rosa_ruolo(ruolo,id_squadra,export=0):
    config = get_config()
    if config.raggruppa_portieri == 1 and ruolo == 'P' and export == 0:
        return db.session.query(Squadre.id.label('id_fanta_squadra'),
                                  Squadre.nome.label('fanta_squadra'),
                                  Listone.id.label('id_giocatore'),
                                  Listone.nome_giocatore,
                                  Listone.squadra,
                                  Listone.ruolo,
                                  Listone.campioncino,
                                  Acquisti.crediti,
                                    Acquisti).join(Listone,Listone.id==Acquisti.id_giocatore).join(Squadre,Squadre.id==Acquisti.id_squadra).where(Acquisti.id_squadra==id_squadra,Listone.ruolo==ruolo).group_by(Listone.squadra).all()

    else:

        return db.session.query(Squadre.id.label('id_fanta_squadra'),
                                  Squadre.nome.label('fanta_squadra'),
                                  Listone.id.label('id_giocatore'),
                                  Listone.nome_giocatore,
                                  Listone.squadra,
                                  Listone.ruolo,
                                  Listone.campioncino,
                                  Acquisti.crediti,
                                    Acquisti).join(Listone,Listone.id==Acquisti.id_giocatore).join(Squadre,Squadre.id==Acquisti.id_squadra).where(Acquisti.id_squadra==id_squadra,Listone.ruolo==ruolo).all()

