'''
from sqlmodel import SQLModel, Field, Relationship
from ..schemas.scan_results import ScanResultInput

class ScanResult(ScanResultInput, table=True):
    __tablename__="scan_agents"
    id : int = Field(primary_key = True, default=None)
    scan_id = Field(foreign_key="scans.id") # check Ondelete 
    policy_id = Field(foreign_key="policies.id") # check Ondelete
    agent_id = Field(foreign_key="agents.id") # check Ondelete
    result_data: list [ResultData] 
    status: str #The overal status of all the policy scan result
    submitted_at: DATE

    rules : list [Rule]  = Relationship (back_populates="policy", cascade_delete=True)


'''
