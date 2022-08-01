from fastapi import APIRouter
from .fanta import router as Fanta
from .listone import router as Listone
from .svincolati import router as Svincolati
from .acquisti import router as Acquisti

router = APIRouter(prefix='/export')
router.include_router(Fanta)
router.include_router(Listone)
router.include_router(Svincolati)
router.include_router(Acquisti)