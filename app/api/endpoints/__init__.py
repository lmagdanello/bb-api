# app/api/endpoints/__init__.py

from fastapi import APIRouter
from . import node, group

router = APIRouter()

router.include_router(node.router, prefix="/nodes", tags=["nodes"])
router.include_router(group.router, prefix="/groups", tags=["groups"])
