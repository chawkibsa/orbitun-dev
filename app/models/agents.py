from sqlmodel import SQLModel, Field, Relationship
from ..schemas.agents import AgentInput
#from .tenants import Tenant

class Agent(AgentInput, table=True):
    __tablename__="agents"
    id : int = Field(primary_key = True, default=None)
    tenant_id : int = Field(foreign_key="tenants.id")

    tenant: "Tenant"  = Relationship(back_populates="agents")






