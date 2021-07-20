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
    soup = BeautifulSoup(decoded_content)
    for img in soup.find('header').findAll('img', {'height': "48"}):
        squadra=img.get('title').capitalize()+".png"
        img_url="https://www.legaseriea.it"+img.get('src')
        output = 'stemmi/' + squadra
        if not os.path.exists(output):
            r = requests.get(img_url, allow_redirects=True)
            open(output, 'wb').write(r.content)
            print("Download {}".format(squadra))



@app.command()
def import_listone(download_campioncini: Optional[int] = typer.Option(0,help="Scarica i campioncini in locale")):
    link_lista_campioncini = 'https://www.fantacalcio.it/servizi/lista.ashx'
    engine = create_engine(os.environ['CONNECTION_STRING'], echo=False)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    if download_campioncini != 0:
        typer.echo("Cancello i campioncini")
        for i in glob.glob("./campioncini/*.jpg"):
            os.remove(i)
        typer.echo("Scarico i campioncini")
    with requests.Session() as s:
        download = s.get(link_lista_campioncini)

        decoded_content = download.content.decode('utf-8')

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
                        # print("Download di {}".format(os.path.basename(row[15])))
                        # typer.echo("Download di {}".format(os.path.basename(row[15])))
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
    ready=0
    while ready==0:
        try:
            engine = create_engine(os.environ['CONNECTION_STRING'], echo=False).connect()
            ready=1
        except (SQLAlchemyError, DBAPIError) as e:
            print('Mysql not ready...Wait')
            time.sleep(2)



    if not database_exists(engine.url):
        create_db()

    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    if session.query(func.count(Listone.id)).scalar()==0:
        import_listone(download_campioncini=0)
    uvicorn.run("app:app", host='0.0.0.0', port=5555, reload=True, debug=True, workers=5)

if __name__ == "__main__":
    app()