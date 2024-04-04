from fastapi import APIRouter
from typing import List
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

from core.models import Profile, Node

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

@router.get("/profiles", response_model=List[Profile])
async def get_equipment_profiles():
    """
    Get all Equipment Profiles from Ansible inventory.
    """
    equipment_profiles = []
    for profile in inventory.list_groups():
        profile = Profile(
            name = profile
        )

        equipment_profiles.append(profile)

    return equipment_profiles

@router.get("/profiles/{profile}", response_model=List[Profile])
async def get_profile_details(profile: str):
    """
    Get Equipment Profile details from Ansible inventory.
    """
    
@router.get("/profiles/{profile}/{node}", response_model=List[Node])
async def get_node_details(profile: str, node: str):
    """
    Get details of a specific node.
    """
    target = []
    for host in inventory.groups[profile].get_hosts():
        if host.name == node:
            host = Node(
                name = host.name,
                profile = profile,
                bmc = host.vars['bmc'],
                network_interfaces = host.vars['network_interfaces']
        )
                
            target.append(host)

    return target
