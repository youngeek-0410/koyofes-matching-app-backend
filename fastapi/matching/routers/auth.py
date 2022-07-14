from matching.api import AuthAPI
from matching.schemas import LoginSchema, Token

from fastapi import APIRouter, Depends, Request

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(request: Request, schema: LoginSchema = Depends()):
    return AuthAPI.login(request, schema)
