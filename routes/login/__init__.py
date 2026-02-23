from fastapi import Request, APIRouter, Query
from services.supabase_service import login_user
from models.schemas import LoginRequest
from tool import logger

login_route = APIRouter(prefix="/login")


@login_route.post("/")
def login(data: LoginRequest):
    response = login_user(data.email, data.password)
    if response.get("error"):
        raise HTTPException(status_code=401, detail=response["error"])
    return response
