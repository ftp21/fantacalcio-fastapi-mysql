from fastapi import FastAPI,WebSocket
from dotenv import dotenv_values,load_dotenv
from app.tasks.push_update import push_update

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper
from app.endpoints import router as Routes
from fastapi.staticfiles import StaticFiles


def get_application() -> FastAPI:
    config = dotenv_values()
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



    app.add_middleware(DBSessionMiddleware, db_url=config['CONNECTION_STRING'])
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

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                print(connection)


'''
    WEBSOCKET
'''
manager = ConnectionManager()
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()

    except WebSocketDisconnect:
        manager.disconnect(websocket)




