from fastapi import APIRouter
from pydantic import BaseModel
from api.schemas.auth import AuthRequest
from utils.supabase_client import supabase
from fastapi import HTTPException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(request: AuthRequest):
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        return {"message": "Registration successful." , "user": response.user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Registration failed") from e
    

@router.post("/login")
async def login(request: AuthRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))