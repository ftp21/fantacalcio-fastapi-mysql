from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware

from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper
from app.endpoints import router as Routes
from fastapi.staticfiles import StaticFiles

import logging
app = FastAPI(
    title="Fantacalcio Backend",

)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DBSessionMiddleware, db_url='mysql://root:my-secret-pw@192.168.253.64/fantacalcio')
app.include_router(Routes)
app.mount("/stemmi", StaticFiles(directory="stemmi"), name="stemmi")
app.mount("/campioncini", StaticFiles(directory="campioncini"), name="campioncini")
app.mount("/backup", StaticFiles(directory="backup"), name="backup")



@app.on_event("startup")
async def startup_event():
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # logger.handlers= gunicorn_logger
    # logger.setLevel(gunicorn_logger.level)
    return ""

