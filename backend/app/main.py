# Backend FAPI
# This is mt helpers definition for the api requrest
# - /api/v1/auth/login = returns a demo token
# - /api/v1/devices = protected GET, returns a fake list
# - /api/v1/commands = protected POST, echoes a queued command

# libs
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Header
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path

app = FastAPI(title="SAC with PLC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Device(BaseModel):
    id: str
    name: str
    type: str
    status: str
    site: Optional[str] = None
    created_at: datetime

class CreateCommand(BaseModel):
    device_id: str
    command: str
    params: Optional[dict] = None

class CommandResponse(BaseModel):
    id: str
    status: str
    device_id: str
    command: str
    submitted_at: datetime

# db in memory (test db)
DEVICES = [
    Device(id="dev_1", name="Stepper Motors", type="plc",   status="online",  site="Lab-1", created_at=datetime.utcnow()),
    Device(id="dev_2", name="Stack Lights",   type="robot", status="offline", site="Lab-2", created_at=datetime.utcnow()),
]

def get_current_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    if token != "demo-token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token

# Routes

@app.get("/healths")
def healths():
    return {"status": "ok"}

@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(body: LoginRequest):
    if body.email and body.password:
        return TokenResponse(access_token="test-token")
    raise HTTPException(status_code=400, detail="Invalid credentials")

@app.get("/api/v1/devices", response_model=List[Device])
def list_devices(token: str = Depends(get_current_token)):
    # oken must be sent
    return DEVICES

@app.post("/api/v1/commands", response_model=CommandResponse)
def create_command(cmd: CreateCommand, token: str = Depends(get_current_token)):
    # Setting jobs in queus
    return CommandResponse(
        id="cmd_001",
        status="queued",
        device_id=cmd.device_id,
        command=cmd.command,
        submitted_at=datetime.utcnow(),
    )


@app.get("/api/v1/recognition/status")
def recognition_status():
    """Return the latest recognition status written by the recognition script.
    The recognition script wries to `backend/app/recognition_status.json`.
    """
    status_file = Path(__file__).parent / "recognition_status.json"
    if not status_file.exists():
        default = {
            "name": "Unknown",
            "status": "idle",
            "updated_at": datetime.utcnow().isoformat(),
        }
        try:
            status_file.write_text(json.dumps(default))
        except Exception:
            pass
        return default

    try:
        data = json.loads(status_file.read_text())
        return data
    except Exception:
        return {"name": "Unknown", "status": "error", "updated_at": datetime.utcnow().isoformat()}
