from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.routes.rose.utils import get_rosa
from app.routes.squadre.views import get_squadre
import xlsxwriter
router = APIRouter(tags=["Scarica il file per l'import su Fantacalcio"])


@router.get('/acquisti')
async def export_fanta():
    workbook = xlsxwriter.Workbook('tmp/Acquisti.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ['Nome Giocatore', 'Squadra', 'Crediti','Ruolo','Fantasquadra'], workbook.add_format({'bold': True}))
    row = 1

    squadre = get_squadre()

    for squadra in squadre:
        rosa = get_rosa(squadra.id, 1)
        for giocatore in rosa.portieri,rosa.difensori,rosa.centrocampisti,rosa.attaccanti:
            for g in giocatore:
                worksheet.write_row(row, 0, [str(g.nome_giocatore).rstrip(), str(g.squadra).rstrip(),
                                                                              str(g.crediti).rstrip(), str(g.ruolo).rstrip(),str(g.fanta_squadra).rstrip()])
                row+=1
    worksheet.autofilter('A1:E{}'.format(row))

    workbook.close()
    return FileResponse('tmp/Acquisti.xlsx', filename="Acquisti.xlsx")



