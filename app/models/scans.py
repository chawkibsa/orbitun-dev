from sqlmodel import SQLModel, Field, Relationship
from ..schemas.scans import ScanInput
from .scan_endpoints_link import ScanEndpointLink
from .scan_policies_link import ScanPolicyLink
#from .scan_policies import ScanPolicy


class Scan(ScanInput, table=True):
    __tablename__="scans"
    id : int = Field(primary_key = True, default=None)
    status : str = Field(default="created")
    
    endpoints : list["Endpoint"] = Relationship(back_populates="scans", link_model=ScanEndpointLink)
    policies: list["Policy"] = Relationship(back_populates="scans", link_model=ScanPolicyLink)


