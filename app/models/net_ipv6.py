from sqlmodel import SQLModel, Field, Relationship
from ..schemas.net_ipv6 import NetIpv6Base
#from .scan_policies import ScanPolicy
#from .endpoints import Endpoint


class NetIpv6(NetIpv6Base, table=True):
    __tablename__="ipv6_network_interfaces"
    id : int = Field(primary_key = True, default=None)
    endpoint_id : int = Field(foreign_key="endpoints.id")

    endpoint : "Endpoint" = Relationship(back_populates="ipv6_addresses")


    