from sqlmodel import SQLModel
from .policies import PolicyOutput
from .endpoints import EndpointOutput
#from .agents import AgentOutput

class ScanInput(SQLModel):
    name: str
    description: str

class ScanOutput(ScanInput):
    id:int
    status: str 
    
    policies: list["PolicyOutput"] | None = []
    endpoints : list["EndpointOutput"] | None = []
    #tenant : list["AgentOutput"] | None = []

