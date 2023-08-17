from app.socketio_manager import sio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from middleware import LoggingMiddleware
from routers import messages
from routers import users, conversations, participants, messages, invitations
import socketio
import uvicorn

app = FastAPI()
sio_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)


# for the frontend, figure out what to do with this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(users.router, prefix="/users")
app.include_router(conversations.router, prefix="/conversations")
app.include_router(participants.router)
app.include_router(messages.router)
app.include_router(invitations.router, prefix="/invitations")


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
