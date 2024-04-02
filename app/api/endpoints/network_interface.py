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

@router.get("/network", response_model=List[Profile])
async def get_networks():
    """
    Get all Networks from Ansible inventory.
    """

@router.get("/{network}/ip4", response_model=List[Node])
async def get_network_ip():
    """
    Get all IP Addresses.
    """

@router.get("/{network}/mac", response_model=List[Node])
async def get_network_ips():
    """
    Get all MAC Addresses.
    """

@router.get("/{network}/{node}", response_model=List[Node])
async def get_network_ips(node: str):
    """
    Get network information of a specific node.
    """

@router.get("/{network}/{ip4}", response_model=List[Node])
async def get_network_ips(ip4: str):
    """
    Get network information of a specific IP address.
    """

@router.get("/{network}/{mac}", response_model=List[Node])
async def get_network_ips(mac: str):
    """
    Get network information of a specific MAC address.
    """
