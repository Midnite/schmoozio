from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routers import users, conversations, participants, messages, invitations, websocket
import uvicorn
from database import get_db

app = FastAPI()

# for the frontend, figure out what to do with this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(users.router, prefix="/users")
app.include_router(conversations.router, prefix="/conversations")
app.include_router(participants.router)
app.include_router(messages.router)
app.include_router(invitations.router, prefix="/invitations")
app.include_router(websocket.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
