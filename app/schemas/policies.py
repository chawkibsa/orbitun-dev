from sqlmodel import SQLModel
from .rules import RuleOutput

class PolicyInput(SQLModel):
    name: str

class PolicyOutput(PolicyInput):
    id : int 
    rules: list[RuleOutput] = []
    