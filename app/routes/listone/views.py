import os

from fastapi import APIRouter, File, UploadFile,HTTPException
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from app.database.listone.model import Listone
from app.routes.listone.schemas.default import Listone as ListoneSchema
from typing import List
from cli import import_listone
from fastapi_sqlalchemy import db
router = APIRouter(tags=['View Listone'])

@router.get('/listone', response_model=List[ListoneSchema],name="Listone",)
def listone() :
    '''Get del listone'''
    return db.session.query(Listone).all()


@router.post('/listone',name="Upload Listone")
async def upload_listone(file: UploadFile = File(...)):
    '''Upload del listone'''

    #
    # delete
    # from mescola;
    # delete
    # from listone;
    # delete
    # from acquisti;
    if file.content_type == "text/csv":
        db.session.execute("delete from mescola ;")
        db.session.execute("delete from acquisti ;")
        db.session.execute("delete from listone ;")

        db.session.commit()
        db.session.close()
        contents = await file.read()
        with open('tmp/listone.csv', 'wb') as f:
            f.write(contents)
        ruoli,total=import_listone(download_campioncini=0)
        os.remove('tmp/listone.csv')
        f.close()
        if len(ruoli)==4:
            return {
                "attaccanti" : ruoli[0][0],
                "centrocampisti" : ruoli[1][0],
                "difensori": ruoli[2][0],
                "portieri": ruoli[3][0],
                "totale": total
            }
        else:
            return HTTPException(status_code=400, detail="Invalid file format")
    else:
        os.remove('tmp/listone.csv')
        return HTTPException(status_code=400, detail="File type not supported")