from sqlmodel import SQLModel

class NetIpv4Base(SQLModel):
    address: str


class NetIpv4Output(NetIpv4Base):
    id: int
