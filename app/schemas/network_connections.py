from sqlmodel import SQLModel

class NetworkConnectionsBase(SQLModel):
    id: int
    fd: str
    family: str
    type: str
    local_address: str
    remote_address: str
    status: str
    pid: str
