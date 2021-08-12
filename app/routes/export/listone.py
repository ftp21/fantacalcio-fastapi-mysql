from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.routes.listone.views import listone
import xlsxwriter

router = APIRouter(tags=['Export Listone'])

@router.get('/listone')
def export_listone():
    lista=listone()
    workbook = xlsxwriter.Workbook('tmp/Listone.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0,0,['ID','Nome','Squadra','Ruolo'],workbook.add_format({'bold': True}))
    row=1
    worksheet.autofilter('A1:D{}'.format(len(lista)+1))
    for giocatore in lista:
        worksheet.write_row(row,0,[str(giocatore.id).rstrip(),str(giocatore.nome_giocatore).rstrip(),str(giocatore.squadra).rstrip(),str(giocatore.ruolo).rstrip()])
        row+=1
    workbook.close()
    return FileResponse('tmp/Listone.xlsx', filename="Listone.xlsx")
