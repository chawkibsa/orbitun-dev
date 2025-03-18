from sqlmodel import SQLModel
from .tenants import TenantOutput
#from .scans import ScanInput

class AgentInput(SQLModel):
    tenant_id : int
    is_persistent: bool = False
    status: str = "offline"
    last_heartbeat: str #Time of the last heartbeat
    created_at: str # Creation time
    updated_at: str # Update time

class AgentOutput(AgentInput):
    id : int
    tenant: TenantOutput | None = []


    
    #scans : list [ScanInput] | None = []

