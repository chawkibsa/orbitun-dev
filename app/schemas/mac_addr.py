from sqlmodel import SQLModel

class MacAddrBase(SQLModel):
    address: str


class MacAddrOutput(MacAddrBase):
    id: int
