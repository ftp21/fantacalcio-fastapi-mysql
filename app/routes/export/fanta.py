from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.routes.rose.utils import get_rosa
from app.routes.squadre.views import get_squadre
router = APIRouter(tags=["Scarica il file per l'import su Fantacalcio"])


@router.get('/fanta')
async def export_fanta():

    squadre=get_squadre()
    file=open('tmp/export.csv','w')
    for squadra in squadre:
        rosa=get_rosa(squadra.id)
        file.write("$,$,$\n")
        for portieri in rosa.portieri:
            file.write("{},{},{}\n".format(squadra.nome,portieri.id_giocatore,portieri.crediti))
        for difensori in rosa.difensori:
            file.write("{},{},{}\n".format(squadra.nome,difensori.id_giocatore,difensori.crediti))
        for centrocampisti in rosa.centrocampisti:
            file.write("{},{},{}\n".format(squadra.nome,centrocampisti.id_giocatore,centrocampisti.crediti))
        for attaccanti in rosa.attaccanti:
            file.write("{},{},{}\n".format(squadra.nome,attaccanti.id_giocatore,attaccanti.crediti))
    file.close()
    return FileResponse('tmp/export.csv',filename="export_fantacalcio.csv")