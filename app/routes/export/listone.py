from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.routes.listone.views import listone
router = APIRouter(tags=['Export Listone'])

@router.get('/listone')
def export_listone():
    lista=listone()
    csv_listone = open("tmp/Listone.csv", 'w')
    csv_listone.write("ID;Nome;Squadra;Ruolo\n")
    for giocatore in lista:
        row="{};{};{};{}\n".format(str(giocatore.id).rstrip(),str(giocatore.nome_giocatore).rstrip(),str(giocatore.squadra).rstrip(),str(giocatore.ruolo).rstrip())
        csv_listone.write(row)
    csv_listone.close()
    return FileResponse('tmp/Listone.csv',filename="Listone.csv")
