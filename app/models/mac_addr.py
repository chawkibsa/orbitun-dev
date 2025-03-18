from sqlmodel import SQLModel, Field, Relationship
from ..schemas.mac_addr import MacAddrBase
#from .scan_policies import ScanPolicy
#from .endpoints import Endpoint


class MacAddr(MacAddrBase, table=True):
    __tablename__="mac_interfaces"
    id : int = Field(primary_key = True, default=None)
    endpoint_id : int = Field(foreign_key="endpoints.id")

    endpoint : "Endpoint" = Relationship(back_populates="mac_addresses")


    