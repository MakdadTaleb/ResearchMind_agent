from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.supabase_client import supabase

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        response = supabase.auth.get_user(token)
        if not response or not response.user :
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return response.user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from e    