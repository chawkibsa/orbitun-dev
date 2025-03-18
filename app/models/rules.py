from sqlmodel import SQLModel, Field, Relationship
#from .rules import RuleInput
#from .policies import Policy
from .variables import Variable
from ..schemas.rules import RuleInput

class Rule(RuleInput, table=True):
    __tablename__ = "rules"
    id: int = Field(default=None, primary_key=True)
    policy_id: int = Field(foreign_key="policies.id", ondelete="CASCADE")
    path: str | None = Field()
    
    variables : list[Variable]  = Relationship (back_populates="rule", cascade_delete=True)
    policy : "Policy" = Relationship(back_populates="rules")
    #results : "resultData" = Relationship


