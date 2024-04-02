# app/core/models.py

"""
This module defines the data models for our inventory API.
"""

from pydantic import BaseModel
from typing import List, Optional, Dict

class NetworkInterface(BaseModel):
    """
    Represents a network interface of a node.
    """
    interface: str
    ip4: str
    mac: Optional[str]
    network: str

class Node(BaseModel):
    """
    Represents a node in the inventory.
    """
    name: str
    profile: str
    bmc: Optional[dict]
    network_interfaces: List[NetworkInterface]

class Profile(BaseModel):
    """
    Represents a Equipment Profile in the inventory.
    """
    name: str