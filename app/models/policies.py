from sqlmodel import SQLModel, Field, Relationship
from ..schemas.policies import PolicyInput
from .rules import Rule
from .scan_policies_link import ScanPolicyLink
from .scans import Scan
from .tenants import Tenant


class Policy(PolicyInput, table=True):
    __tablename__="policies"
    id : int = Field(primary_key = True, default=None)
    tenant_id : int = Field(foreign_key="tenants.id")
    
    tenant: Tenant = Relationship(back_populates="policies")
    rules : list [Rule]  = Relationship (back_populates="policy", cascade_delete=True)
    scans : list [Scan] = Relationship(back_populates="policies", link_model=ScanPolicyLink)
    



