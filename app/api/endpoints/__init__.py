# app/api/endpoints/__init__.py

from fastapi import APIRouter
from . import node

router = APIRouter()

router.include_router(node.router, prefix="/nodes", tags=["nodes"])
