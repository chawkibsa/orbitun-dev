from sqlmodel import SQLModel, Field, Relationship
from ..schemas.tenants import TenantInput
from .agents import Agent

class Tenant(TenantInput, table=True):
    __tablename__="tenants"
    id : int = Field(primary_key = True, default=None)

    agents: list["Agent"] = Relationship(back_populates="tenant")
