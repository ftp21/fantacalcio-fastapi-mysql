from fastapi import APIRouter,Form
from .utils import can_i_buy,svincolatore
from app.routes.configurazione.utils import get_config
from app.database.acquisti.model import Acquisti
from app.database.listone.model import Listone
from fastapi import HTTPException
from sqlalchemy import text
from fastapi_sqlalchemy import db  # an object to provide global access to a database session


router = APIRouter(tags=['Gestisce acquisti e svincoli'])
@router.post('/acquista/{id_giocatore}')
def acquista_giocatore(
        id_giocatore: int,
        crediti: int = Form(...),
        id_squadra: int = Form(...)
    ):
    config = get_config()
    message = ""
    message = can_i_buy(id_squadra, crediti, id_giocatore)
    if message == "":

        giocatore_acquisti = db.session.query(Acquisti).filter(Acquisti.id_giocatore == id_giocatore).first()
        giocatore = db.session.query(Listone).get(id_giocatore)
        if config.raggruppa_portieri == 1 and giocatore.ruolo=='P':
            id_giocatori_squadra=db.session.query(Listone.id).filter(Listone.ruolo=='P',Listone.squadra==giocatore.squadra).all()
            first=1

            for id in id_giocatori_squadra:

                if first==1:
                    if giocatore_acquisti != None:
                        print(id)
                        db.session.delete(db.session.query(Acquisti).filter(Acquisti.id_giocatore==int(id.id)).one())
                        db.session.commit()
                    db.session.add(Acquisti(
                        id_giocatore=int(id.id),
                        crediti=crediti,
                        id_squadra=id_squadra,
                        ora=text("now()")
                    ))
                    first=0
                else:
                    if giocatore_acquisti != None:
                        db.session.delete(db.session.query(Acquisti).filter(Acquisti.id_giocatore==int(id.id)).one())
                        db.session.commit()
                    db.session.add(Acquisti(
                        id_giocatore=int(id.id),
                        crediti=0,
                        id_squadra=id_squadra,
                        ora=text("now()")
                    ))
            db.session.commit()
            return id_giocatore

        if giocatore_acquisti != None:
            check_acquisti=db.session.query(Acquisti).filter(Acquisti.id_giocatore==giocatore_acquisti.id_giocatore).first()
            if check_acquisti !=None:
                db.session.delete(check_acquisti)
                db.session.commit()
        acquisto = Acquisti(
            id_giocatore=id_giocatore,
            crediti=crediti,
            id_squadra=id_squadra,
            ora=text("now()")
        )
        db.session.add(acquisto)
        db.session.commit()
        return id_giocatore
    raise HTTPException(400,detail=message)

@router.post('/svincola/{id_giocatore}')
def svincola_giocatore(
        id_giocatore: int,
    ):
    return svincolatore(id_giocatore)
    # config = get_config()
    #
    # giocatore_svincolare = db.session.query(Acquisti).filter(Acquisti.id_giocatore == id_giocatore).first()
    # if giocatore_acquisti != None:
    #     '''
    #            TODO: AGGIUNGERE SVINCOLO PORTIERI MULTIPLI
    #     '''
    #     db.session.delete(giocatore_svincolare)
    #     db.session.commit()
    #     return id_giocatore
    # return HTTPException(400,detail="Giocatore non acquistato")