from sqlmodel import SQLModel, Field, Relationship
from ..schemas.variables import VariableInput
#from .rules import Rule

class Variable(VariableInput, table=True):
    __tablename__ = "variables"
    id : int = Field(default= None, primary_key=True)
    rule_id : int = Field(foreign_key="rules.id", ondelete="CASCADE")
    rule : "Rule" = Relationship(back_populates="variables")
