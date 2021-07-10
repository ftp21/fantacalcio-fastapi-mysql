from fastapi import APIRouter
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from app.database.listone.model import Listone
from app.routes.listone.schemas.default import Listone as ListoneSchema
from typing import List
router = APIRouter(tags=['View Listone'])

@router.get('/listone', response_model=List[ListoneSchema],name="Listone",)
def listone() :
    '''Get del listone'''
    return db.session.query(Listone).all()