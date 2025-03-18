from sqlmodel import SQLModel, Field, Relationship
from ..schemas.endpoints import EndpointBase #EndpointInput
from .scan_endpoints_link import ScanEndpointLink
from .scans import Scan
from .net_ipv4 import NetIpv4
from .net_ipv6 import NetIpv6
from .mac_addr import MacAddr
#from .agents import Agent

class Endpoint(EndpointBase, table=True):
    __tablename__="endpoints"
    id : int = Field(primary_key = True, default=None)
    hostname: str = Field(default=None)
    device_type: str = Field(default=None)#Workstation , Server
    os_type: str = Field(default=None) #Operating system of the machine 
    os_version: str = Field(default=None)
    created_at: str = Field(default=None) # The creation of the endpoint (the registration of the endpoint in the database must be the same as the registration of the agent)
    updated_at: str = Field(default=None)
#    agent_id : int = Field(foreign_key= "agents.id", ondelete="CASCADE")

    scans : list[Scan] = Relationship(back_populates="endpoints", link_model=ScanEndpointLink)
    ipv4_addresses: list[NetIpv4] = Relationship(back_populates="endpoint")
    ipv6_addresses: list[NetIpv6] = Relationship(back_populates="endpoint")
    mac_addresses: list[MacAddr] = Relationship(back_populates="endpoint")



    #agent : list[Agent] = Relationship(back_populates="endpoint")