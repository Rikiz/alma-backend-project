from fastapi import APIRouter
from . import public, internal


api_router = APIRouter()
api_router.include_router(public.router, prefix="/public", tags=["public"])
api_router.include_router(internal.router, prefix="/internal", tags=["internal"])