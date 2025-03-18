from sqlmodel import SQLModel

class NetIpv6Base(SQLModel):
    address: str

class NetIpv6Output(NetIpv6Base):
    id: int
