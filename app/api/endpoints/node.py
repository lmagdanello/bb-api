from fastapi import APIRouter
from typing import List
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

from core.models import Node

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

@router.get("/nodes")
async def get_nodes():
    """
    Get all nodes from Ansible inventory.
    """
    nodes = set()
    for profile in inventory.list_groups():
        hosts = inventory.groups[profile].get_hosts()
        for node in hosts:
            nodes.add(node.name)
    return list(nodes)
