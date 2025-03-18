from sqlmodel import SQLModel, Field, Relationship
from ..schemas.scan_policies import ScanPolicyInput

class ScanPolicyLink(ScanPolicyInput, table=True):
    __tablename__="scan_policies"
    scan_id : int | None  = Field(default= None, foreign_key="scans.id", primary_key=True)# check Ondelete
    policy_id : int | None = Field(default= None, foreign_key="policies.id", primary_key=True) # check Ondelete
