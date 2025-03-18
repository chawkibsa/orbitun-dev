from sqlmodel import SQLModel, Field, Relationship

class DefaultVariable(SQLModel, table=True):
    __tablename__ = "defaultvariables"
    id: int = Field(default=None, primary_key=True)
    rule_id: int = Field(foreign_key="defaultrules.id", ondelete="CASCADE")
    variable: str
    variable_value: str
    default_rule : "DefaultRule" = Relationship(back_populates="default_variables")

class DefaultRule(SQLModel, table=True):
    __tablename__ = "defaultrules"
    id: int = Field(default=None, primary_key=True)
    name: str
    path: str | None = Field()

    default_variables: list[DefaultVariable] = Relationship(back_populates = "default_rule", cascade_delete=True)