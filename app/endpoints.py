from fastapi import APIRouter
from app.routes.listone.views import router as Listone
from app.routes.mescola.views import router as Mescola
from app.routes.squadre.views import router as Squadre
from app.routes.estrai.views import router as Estrai
from app.routes.configurazione.views import router as Configurazione
from app.routes.rose.views import router as Rosa
from app.routes.mercato.views import router as Mercato
from app.routes.svincolati.views import router as Svincolati
from app.routes.status.views import router as Status


router = APIRouter(prefix='/api/v1')
router.include_router(Listone)
router.include_router(Mescola)
router.include_router(Squadre)
router.include_router(Estrai,prefix='/estrai')
router.include_router(Configurazione)
router.include_router(Rosa)
router.include_router(Mercato,prefix='/mercato')
router.include_router(Svincolati)
router.include_router(Status)


