# app/api/endpoints/__init__.py

from fastapi import APIRouter
from . import equipment_profile, node

router = APIRouter()

router.include_router(node.router, tags=["nodes"])
router.include_router(equipment_profile.router, tags=["profiles"])
