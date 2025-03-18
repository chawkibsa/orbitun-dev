from sqlmodel import SQLModel
from .net_ipv4 import NetIpv4Output,NetIpv4Base
from .net_ipv6 import NetIpv6Output, NetIpv6Base
from .mac_addr import MacAddrOutput, MacAddrBase
#from .agents import AgentBase

# Used for user to modify the name and the description of the endpoint
class EndpointBase(SQLModel):
    name: str
    description: str | None = None

# Used for the machine agent to connect with the server though this schema, a further parsing should be made by the server
class EndpointInput(EndpointBase):
    hostname: str
    device_type: str #Workstation , Server
    os_type: str #Operating system of the machine 
    os_version: str # The version of the operating 
    ipv4_addresses: list[NetIpv4Base] |None 
    ipv6_addresses: list[NetIpv6Base] | None 
    mac_addresses: list[MacAddrBase] | None 
    


class EndpointOutput(EndpointInput):
    created_at: str | None # The creation of the endpoint (the registration of the endpoint in the database must be the same as the registration of the agent)
    updated_at: str | None # Record of the change of any of the previous fields
    id : int
    ipv4_addresses: list[NetIpv4Output] |None = []
    ipv6_addresses: list[NetIpv6Output] | None = []
    mac_addresses: list[MacAddrOutput] | None = []
    

    #agent: list[AgentBase] = []



