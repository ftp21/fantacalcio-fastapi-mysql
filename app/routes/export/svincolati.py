from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.routes.svincolati.views import get_svincolati
import xlsxwriter

router = APIRouter(tags=['Export Svincolati'])

@router.get('/svincolati')
def export_svincolati():
    lista=get_svincolati()
    workbook = xlsxwriter.Workbook('tmp/Svincolati.xlsx')





    worksheet = workbook.add_worksheet('Portieri')
    worksheet.write_row(0, 0, ['ID', 'Nome', 'Squadra', 'Ruolo'], workbook.add_format({'bold': True}))
    row = 1
    for portieri in lista.portieri:
        worksheet.write_row(row, 0,[portieri.id, portieri.nome_giocatore,portieri.squadra,portieri.ruolo])
        row+=1
    worksheet = workbook.add_worksheet('Difensori')
    worksheet.write_row(0, 0, ['ID', 'Nome', 'Squadra', 'Ruolo'], workbook.add_format({'bold': True}))
    row = 1
    for difensori in lista.difensori:
        worksheet.write_row(row, 0, [difensori.id, difensori.nome_giocatore,difensori.squadra,difensori.ruolo])
        row += 1
    worksheet = workbook.add_worksheet('Centrocampisti')
    worksheet.write_row(0, 0, ['ID', 'Nome', 'Squadra', 'Ruolo'], workbook.add_format({'bold': True}))
    row = 1
    for centrocampisti in lista.centrocampisti:
        worksheet.write_row(row, 0, [centrocampisti.id, centrocampisti.nome_giocatore, centrocampisti.squadra, centrocampisti.ruolo])
        row += 1
    worksheet = workbook.add_worksheet('Attaccanti')
    worksheet.write_row(0, 0, ['ID', 'Nome', 'Squadra', 'Ruolo'], workbook.add_format({'bold': True}))
    row = 1
    for attaccanti in lista.attaccanti:
        worksheet.write_row(row, 0, [attaccanti.id, attaccanti.nome_giocatore, attaccanti.squadra,attaccanti.ruolo])
        row += 1
    workbook.close()
    return FileResponse('tmp/Svincolati.xlsx',filename="Svincolati.xlsx")
