from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.routes.svincolati.views import get_svincolati
router = APIRouter(tags=['Export Svincolati'])

@router.get('/svincolati')
def export_svincolati():
    lista=get_svincolati()
    csv_svincolati = open("tmp/Svincolati.csv", 'w')
    csv_svincolati.write("ID;Nome;Squadra;Ruolo\n")
    for portieri in lista.portieri:
        csv_svincolati.write("{};{};{};{}\n".format(portieri.id, portieri.nome_giocatore,portieri.squadra,portieri.ruolo))
    for difensori in lista.difensori:
        csv_svincolati.write("{};{};{};{}\n".format(difensori.id, difensori.nome_giocatore,difensori.squadra,difensori.ruolo))
    for centrocampisti in lista.centrocampisti:
        csv_svincolati.write("{};{};{};{}\n".format(centrocampisti.id, centrocampisti.nome_giocatore,centrocampisti.squadra,centrocampisti.ruolo))
    for attaccanti in lista.attaccanti:
        csv_svincolati.write("{};{};{};{}\n".format(attaccanti.id, attaccanti.nome_giocatore,attaccanti.squadra,attaccanti.ruolo))

    csv_svincolati.close()
    return FileResponse('tmp/Svincolati.csv',filename="Svincolati.csv")
