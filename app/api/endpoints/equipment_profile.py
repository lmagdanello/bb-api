# Description: Equipment Profile API endpoints.

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

@router.post("/profiles/{profile}")
async def create_equipment_profile(profile: str):
    """
    Create a new Equipment Profile.
    """

    inventory.add_group(profile)
    return (f"Profile {profile} created.")

@router.delete("/profiles/{profile}")
async def delete_equipment_profile(profile: str):
    """
    Delete an Equipment Profile.
    """
    inventory.remove_group(profile)
    return (f"Profile {profile} deleted.")

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

@router.post("/profiles/{profile}/{node}")
async def create_node_if_not_exists(profile: str, node: str):
    """
    Create a new Node inside an Equipment Profile.
    """
    equipment_profiles = await get_equipment_profiles()
    if profile not in [p.name for p in equipment_profiles]:
        await create_equipment_profile(profile)
    inventory.add_host(host=node, group=profile)
    return (f"Node {node} created in profile {profile}.")

@router.delete("/profiles/{profile}/{node}")
async def delete_node(profile: str, node: str):
    """
    Delete a Node from an Equipment Profile.
    """
    inventory.groups[profile].remove_host(node)
    return (f"Node {node} deleted from profile {profile}.")