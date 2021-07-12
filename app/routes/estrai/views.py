from fastapi import APIRouter,BackgroundTasks
from .schemas.estratto import Estratto,Info
from .utils import get_avanti,get_indietro
router = APIRouter(tags=['Estrazione'])
from app.tasks.push_update import push_update


@router.get('/avanti')
def avanti(background_tasks: BackgroundTasks) -> Estratto:

    avanti=get_avanti()
    background_tasks.add_task(push_update)
    return avanti


@router.get('/indietro')
def indietro(background_tasks: BackgroundTasks) -> Estratto:
    indietro=get_indietro()
    background_tasks.add_task(push_update)
    return indietro