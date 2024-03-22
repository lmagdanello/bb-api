# app/core/models.py

"""
This module defines the data models for our inventory API.
"""

from pydantic import BaseModel
from typing import List, Optional, Dict

class Equipment(BaseModel):
    """
    Represents an equipment in the inventory.
    """
    id: int
    name: str
    type: str

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
    group: str
    bmc: dict
    network_interfaces: List[NetworkInterface]

class Group(BaseModel):
    """
    Represents a group of nodes or equipments.
    """
    id: int
    name: str
    nodes: List[Node] = []
    equipments: List[Equipment] = []

