from sqlmodel import SQLModel

class TenantInput(SQLModel):
    name: str 

class TenantOutput(TenantInput):
    id: int 

    
    