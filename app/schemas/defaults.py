from sqlmodel import SQLModel

class DefaultVariableSC(SQLModel):
    id : int
    #default_rule_id : int
    variable : str
    variable_value : str

class DefaultRuleSC(SQLModel):
    id : int
    name : str
    default_variables : list[DefaultVariableSC] = []