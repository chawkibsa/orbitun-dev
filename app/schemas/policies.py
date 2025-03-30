from sqlmodel import SQLModel
from .rules import RuleOutput
from .tenants import TenantOutput


class PolicyInput(SQLModel):
    name: str
    tenant_id: int


class PolicyOutput(PolicyInput):
    id : int 
    tenant: TenantOutput
    rules: list[RuleOutput] = []

class PolicyUpdate(SQLModel):
    name: str|None = None
    tenant_id: int|None = None
    