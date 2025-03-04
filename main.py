import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
from dotenv import load_dotenv
from livekit.api import AccessToken, VideoGrants
from loguru import logger
import datetime

load_dotenv()

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT")

if not LIVEKIT_API_KEY or not LIVEKIT_API_KEY:
    raise ValueError("LIVEKIT_API_KEY and LIVEKIT_SECRET must be set in the .env file")

app = FastAPI()

if ENVIRONMENT == "PROD":
    origins = [
        "https://www.be-vokal.com",
        "https://be-vokal.com",
        "https://www.simsom.com",
        "https://simsom.com"
    ]
elif ENVIRONMENT == "DEV":
    origins = [
        "http://localhost:8081"
    ]
else:
    raise ValueError("ENVIRONMENT must be set to PROD or DEV in the .env file")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenRequest(BaseModel):
    scene_name: str
    participant_name: str
    metadata: Optional[str] = None
    participant_attributes: Optional[Dict[str, str]] = None


def generate_livekit_token(scene_name: str, participant_name: str, metadata: str, participant_attributes: Dict):
    """Generate a LiveKit access token using livekit.api"""

    token = (
        AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) 
        .with_identity(participant_name)
        .with_ttl(datetime.timedelta(minutes=10))
        .with_grants(VideoGrants(room_join=True, room=scene_name, can_update_own_metadata=True))
    )

    if metadata:
        # Set metadata directly as it's already a string
        token = token.with_metadata(metadata)
    if participant_attributes:
        token.set_claim("participantAttributes", participant_attributes)

    return token.to_jwt()


@app.post("/lk-token")
async def generate_token(request: TokenRequest):
    """API Endpoint to generate LiveKit participant tokens"""

    if not request.participant_name:
        raise HTTPException(status_code=400, detail="participant_name is required")
    
    logger.info(f"Generating token for {request.participant_name} in scene {request.scene_name}")

    token = generate_livekit_token(
        request.scene_name,
        request.participant_name,
        request.metadata or "",
        request.participant_attributes or {},
    )

    logger.info(f"Token generated: {token}")

    return {
        "serverUrl": LIVEKIT_URL,
        "sceneName": request.scene_name,
        "participantName": request.participant_name,
        "participantToken": token,
    }

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "alive"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)