from sqlmodel import SQLModel
from .variables import VariableOutput

class RuleInput(SQLModel):
    name: str 

class RuleOutput(RuleInput):
    id: int | None
    #path: str | None
    variables : list[VariableOutput] | None = []