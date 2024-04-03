from fastapi import APIRouter
from typing import List
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

from core.models import Profile, Node, NetworkInterface

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
host_vars = VariableManager(loader=loader, inventory=inventory)

@router.get("/network", response_model=List[NetworkInterface])
async def get_all_network():
    """
    Get all Networks from Ansible inventory.
    """
    
    network_interfaces = []
    for node in inventory.get_hosts():
        host = host_vars.get_vars(host=node)
        for _, network_data in enumerate(host['network_interfaces']):
            interface = network_data.get('interface', None)
            ip4 = network_data.get('ip4', None)
            mac = network_data.get('mac', None)
            network = network_data.get('network', None)
            
            if mac is not None:
                network_interface = NetworkInterface(interface=interface, ip4=ip4, mac=mac, network=network)
            else:
                network_interface = NetworkInterface(interface=interface, ip4=ip4, network=network)

            network_interfaces.append(network_interface)

    return network_interfaces

@router.get("/network/{network}/ip4", response_model=List[str])
async def get_network_ip(network: str):
    """
    Get all IP Addresses in a Network.
    """
    ip_addresses = []
    for node in inventory.get_hosts():
        host = host_vars.get_vars(host=node)
        for _, network_data in enumerate(host['network_interfaces']):
            if network == network_data.get('network'):
                ip4 = network_data.get('ip4')
                if ip4:
                    ip_addresses.append(ip4)

    return ip_addresses

@router.get("/network/{network}/mac", response_model=List[str])
async def get_network_ip(network: str):
    """
    Get all MAC Addresses in a Network.
    """
    mac_addresses = []
    for node in inventory.get_hosts():
        host = host_vars.get_vars(host=node)
        for _, network_data in enumerate(host['network_interfaces']):
            if network == network_data.get('network'):
                mac = network_data.get('mac')
                if mac:
                    mac_addresses.append(mac)

    return mac_addresses

@router.get("/network/{network}/{node}", response_model=List[str])
async def get_network_ip(network: str, node: str):
    """
    Get network information about a specific Node.
    """
    network_interfaces = []
    for n in inventory.get_host(node):
        # NOT WORKING YET!
        # NEED IMPROVEMENT FOR get_vars
        host = host_vars.get_vars(host=inventory.get_host(node))
        for _, network_data in enumerate(host['network_interfaces']):
            if network == network_data.get('network'):
                interface = network_data.get('interface', None)
                ip4 = network_data.get('ip4', None)
                mac = network_data.get('mac', None)
                network = network_data.get('network', None)
                
                if mac is not None:
                    network_interface = NetworkInterface(interface=interface, ip4=ip4, mac=mac, network=network)
                else:
                    network_interface = NetworkInterface(interface=interface, ip4=ip4, network=network)

                network_interfaces.append(network_interface)

    return network_interfaces
