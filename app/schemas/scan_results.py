'''
from sqlmodel import SQLModel, DATE
#from .policies import PolicyOutput
#from .agents import AgentOutput

class ScanResultInput(SQLModel):
    policy_id : int

class ScanResultOutput(ScanResultInput):
    id : int
    policy_id: int 
    agent_id : int 
    result_data: list | None = None
    status: str
    submitted_at: DATE
'''