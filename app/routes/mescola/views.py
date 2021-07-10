from fastapi import APIRouter,Form
from .schemas.parametri import Parametri
from .utils import parse_and_scramble,revese_mescola
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
