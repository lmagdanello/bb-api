from fastapi import APIRouter
from typing import List
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

from core.models import Group, Node

# TEMPORARY!
# Forcing ansible_inventory_path
from dotenv import load_dotenv
import os
load_dotenv()


router = APIRouter()

# Path to the Ansible inventory file
ansible_inventory_path = os.getenv("ansible_inventory_path")
loader = DataLoader()
inventory = InventoryManager(loader=loader, sources=ansible_inventory_path)

@router.get("/", response_model=List[Group])
async def get_groups():
    """
    Get all groups from Ansible inventory.
    """
    groups = []
    for group in inventory.list_groups():
        group = Group(
            name = group
        )

        groups.append(group)
    return groups