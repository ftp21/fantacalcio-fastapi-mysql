from fastapi import APIRouter,Form
from .schemas.parametri import Parametri
from .utils import parse_and_scramble,revese_mescola
from fastapi.responses import FileResponse
from app.database.mescola.model import Mescola
from fastapi_sqlalchemy import db
import xlsxwriter

router = APIRouter(tags=['Gestione Mescola'])



@router.post('/mescola', name="Mescola i giocatori del listone secondo i parametri dati",)
def mescola(
        portieri: bool = Form(...),
        difensori: bool = Form(...),
        centrocampisti: bool = Form(...),
        attaccanti: bool = Form(...),
        alfabetico: bool = Form(...)

    ) -> int:
    return parse_and_scramble(
        Parametri(
            portieri=portieri,
            difensori=difensori,
            centrocampisti=centrocampisti,
            attaccanti=attaccanti,
            alfabetico=alfabetico
        )
    )
@router.get('/mescola', name="Mescola i giocatori del listone secondo i parametri dati",)
def get_config_mescola() -> Parametri:
    return revese_mescola()

@router.get("/mescolati")
def get_mescolati():
    mescola=db.session.execute("select ordine,nome_giocatore,ruolo,squadra from mescola inner join listone on id_giocatore=listone.id;")
    workbook = xlsxwriter.Workbook('tmp/Mescolati.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ['Ordine', 'Nome', 'Squadra', 'Ruolo'], workbook.add_format({'bold': True}))
    row = 1
    worksheet.autofilter('A1:D{}'.format(len(mescola) + 1))
    for giocatore in mescola:
        worksheet.write_row(row, 0, [str(giocatore.ordine).rstrip(), str(giocatore.nome_giocatore).rstrip(),
                                     str(giocatore.squadra).rstrip(), str(giocatore.ruolo).rstrip()])
        row += 1
    workbook.close()
    db.session.commit()
    return FileResponse('tmp/Mescolati.xlsx', filename="Mescolati.xlsx")