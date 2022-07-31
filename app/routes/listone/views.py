import os

from fastapi import APIRouter, File, UploadFile
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from app.database.listone.model import Listone
from app.routes.listone.schemas.default import Listone as ListoneSchema
from typing import List
from cli import import_listone,create_db,import_settings
router = APIRouter(tags=['View Listone'])

@router.get('/listone', response_model=List[ListoneSchema],name="Listone",)
def listone() :
    '''Get del listone'''
    return db.session.query(Listone).all()


@router.post('/listone',name="Upload Listone")
async def upload_listone(file: UploadFile = File(...)):
    '''Upload del listone'''

    create_db()
    import_settings()
    contents = await file.read()
    with open('tmp/listone.csv', 'wb') as f:
        f.write(contents)
    ruoli,total=import_listone(download_campioncini=0)
    os.remove('tmp/listone.csv')
    print(ruoli[0][1])

    return {
        "attaccanti" : ruoli[0][0],
        "centrocampisti" : ruoli[1][0],
        "difensori": ruoli[2][0],
        "portieri": ruoli[3][0],
        "totale": total
    }