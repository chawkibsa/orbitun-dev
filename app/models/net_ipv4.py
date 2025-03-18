from sqlmodel import SQLModel, Field, Relationship
from ..schemas.net_ipv4 import NetIpv4Base
#from .scan_policies import ScanPolicy
#from .endpoints import Endpoint


class NetIpv4(NetIpv4Base, table=True):
    __tablename__="ipv4_network_interfaces"
    id : int = Field(primary_key = True, default=None)
    endpoint_id : int = Field(foreign_key="endpoints.id")

    endpoint : "Endpoint" = Relationship(back_populates="ipv4_addresses")




    