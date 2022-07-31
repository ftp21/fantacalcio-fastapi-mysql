from fastapi import FastAPI,WebSocket,WebSocketDisconnect,BackgroundTasks
from dotenv import dotenv_values,load_dotenv
from app.tasks.push_update import push_update
import os
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper
from app.endpoints import router as Routes
from fastapi.staticfiles import StaticFiles


def get_application() -> FastAPI:
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



    app.add_middleware(DBSessionMiddleware, db_url=os.environ['CONNECTION_STRING'],engine_args={'pool_size':0, 'max_overflow': -1},commit_on_exit=True)
    app.include_router(Routes)
    app.mount("/stemmi", StaticFiles(directory="stemmi"), name="stemmi")
    app.mount("/campioncini", StaticFiles(directory="campioncini"), name="campioncini")
    app.mount("/backup", StaticFiles(directory="backup"), name="backup")




    return app



app=get_application()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass


'''
    WEBSOCKET
'''
manager = ConnectionManager()
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)




