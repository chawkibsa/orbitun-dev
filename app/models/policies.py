from sqlmodel import SQLModel, Field, Relationship
from ..schemas.policies import PolicyInput
from .rules import Rule
from .scan_policies_link import ScanPolicyLink
from .scans import Scan

class Policy(PolicyInput, table=True):
    __tablename__="policies"
    id : int = Field(primary_key = True, default=None)
    
    rules : list [Rule]  = Relationship (back_populates="policy", cascade_delete=True)
    scans : list [Scan] = Relationship(back_populates="policies", link_model=ScanPolicyLink)
    



