from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client
import os

router = APIRouter()

SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_KEY=os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase=create_client(SUPABASE_URL,SUPABASE_KEY)

class Login(BaseModel):
    email:str
    password:str

@router.post("/signup")
async def signup(data:Login):
    res=supabase.auth.sign_up({
        "email":data.email,
        "password":data.password
    })
    return {"user":res.user}

@router.post("/login")
async def login(data:Login):
    res=supabase.auth.sign_in_with_password({
        "email":data.email,
        "password":data.password
    })
    if not res.session:
        raise HTTPException(401,"invalid login")
    return {"session":res.session}
