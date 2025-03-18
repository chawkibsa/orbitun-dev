from sqlmodel import SQLModel


class VariableInput(SQLModel):
    variable : str | None
    variable_value : str | None

class VariableOutput(VariableInput):
    id : int | None