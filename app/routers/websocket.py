from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi import APIRouter
import aioredis

router = APIRouter()

REDIS_URL = "redis://localhost:6379/0"


@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: int):
    await websocket.accept()

    # Connect to Redis asynchronously
    redis = await aioredis.from_url(REDIS_URL)

    # Create a pubsub manager from the Redis connection
    pubsub = redis.pubsub()
    channel_name = f"chat_{conversation_id}"
    await pubsub.subscribe(channel_name)

    try:
        # Listen to the channel for incoming messages
        async for message in pubsub.listen():
            # Check the type of the message
            if message["type"] == "message":
                data = message["data"]
                await websocket.send_text(data.decode("utf-8"))
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(channel_name)
        redis.close()
    await websocket.accept()
    await websocket.send_text("Connected!")
