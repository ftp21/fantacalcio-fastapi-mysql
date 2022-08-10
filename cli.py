import time

import typer,requests,csv,os,glob,uvicorn
from typing import Optional
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError,SQLAlchemyError,DBAPIError
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import func
from bs4 import BeautifulSoup

from app.database import Base
from app.database.listone.model import Listone

app = typer.Typer()
import os
load_dotenv()
@app.command()
def import_stemmi():
    url = "https://www.legaseriea.it/it"
    download = requests.get(url)
    decoded_content = download.content.decode('utf-8')
    soup = BeautifulSoup(decoded_content,features="html.parser")
    for img in soup.find('header').findAll('img', {'height': "48"}):
        squadra=img.get('title').capitalize()+".png"
        img_url="https://www.legaseriea.it"+img.get('src')
        # Fix hellas verona
        name = squadra.split(' ')
        try:
            squadra=name[1].capitalize()
            output = 'stemmi/' + squadra
            if not os.path.exists(output):
                r = requests.get(img_url, allow_redirects=True)
                open(output, 'wb').write(r.content)
                typer.echo("Download {}".format(squadra))
        except IndexError:
            output = 'stemmi/' + squadra
            if not os.path.exists(output):
                r = requests.get(img_url, allow_redirects=True)
                open(output, 'wb').write(r.content)
                typer.echo("Download {}".format(squadra))



@app.command()
def import_listone(download_campioncini: Optional[int] = typer.Option(0,help="Scarica i campioncini in locale")):
    engine = create_engine(os.environ['CONNECTION_STRING'], echo=False)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    if download_campioncini != 0:
        typer.echo("Cancello i campioncini")
        for i in glob.glob("./campioncini/*.jpg"):
            os.remove(i)
        typer.echo("Scarico i campioncini")
    with open("tmp/listone.csv") as s:

        decoded_content = s.read()

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        session.execute('''DELETE FROM listone''')
        session.commit()
        obj = []
        if download_campioncini !=0:
            typer.echo("Scarico {} campioncini".format(len(my_list)))
        # with typer.progressbar(range(len(my_list))) as progress:
        with typer.progressbar(length=len(my_list)) as progress:
            for row in my_list:
                if download_campioncini !=0:
                    campioncino='campioncini/'+os.path.basename(row[15])
                    if not os.path.exists(campioncino):
                        r = requests.get(row[15], allow_redirects=True)
                        open(campioncino, 'wb').write(r.content)
                        campioncino='/'+campioncino
                    progress.update(1)
                else:
                    campioncino=row[15]
                obj.append(Listone(
                    id=row[0],
                    ruolo=row[3],
                    nome_giocatore=row[1],
                    squadra=row[9],
                    campioncino=campioncino
                ))
        if download_campioncini != 0:
            typer.echo("Ho scaricato {} campioncini".format(len(my_list)))
        else:
            typer.echo("Ho importato {} campioncini".format(len(my_list)))
        session.bulk_save_objects(obj)
        session.commit()
    session.close()
    #select count(ruolo),ruolo from listone group by ruolo
    return session.execute('select count(ruolo),ruolo from listone group by ruolo').all(),len(my_list)

@app.command()
def create_db():
    engine = create_engine(os.environ['CONNECTION_STRING'], echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@app.command()
def flush_campioncini():
    typer.echo("Cancello i campioncini")
    for i in glob.glob("./campioncini/*.jpg"):
        os.remove(i)

@app.command('run')
def start_fastapi():
    engine = create_engine(os.environ['CONNECTION_STRING'], echo=False)
    if not database_exists(engine.url):
        create_db()
    if os.path.exists('tmp/listone.csv'):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = Session()
        if session.query(func.count(Listone.id)).scalar()==0:
            import_listone(download_campioncini=0)
        session.close()
    import_settings()


    uvicorn.run("app:app", host='0.0.0.0', port=5555, reload=True, debug=True, workers=5)
@app.command('import-settings')
def import_settings():
    if os.path.exists('import.yaml'):
        typer.echo("Importo le impostazioni dell'asta")
        import yaml
        engine = create_engine(os.environ['CONNECTION_STRING'], echo=False)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = Session()

        with open('import.yaml') as f:
            impostazioni = yaml.safe_load(f)
        from app.database.squadre.model import Squadre
        session.query(Squadre).delete()
        for squadra in impostazioni['squadre']:
            session.add(
                Squadre(
                    nome=squadra,
                    code=''.join(["{}".format(randint(0, 9)) for num in range(0, 5)])
                )
            )
            session.commit()

        from app.database.configurazione.model import Configurazione
        session.query(Configurazione).delete()
        me = Configurazione(
            id=1,
            portieri=impostazioni['impostazioni']['portieri'],
            difensori=impostazioni['impostazioni']['difensori'],
            centrocampisti=impostazioni['impostazioni']['centrocampisti'],
            attaccanti=impostazioni['impostazioni']['attaccanti'],
            raggruppa_portieri=impostazioni['impostazioni']['raggruppa_portieri'],
            crediti_totali=impostazioni['impostazioni']['crediti_totali'],
            nascondi_crediti=impostazioni['impostazioni']['crediti_nascosti'],
        )
        session.add(me)
        session.commit()


if __name__ == "__main__":
    app()