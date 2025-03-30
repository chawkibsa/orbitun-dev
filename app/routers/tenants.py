from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_session
from sqlmodel import Session, select
from ..schemas.tenants import TenantInput, TenantOutput
from ..models.tenants import Tenant


router = APIRouter(prefix="/api/tenants", tags=["Tenants Management"])#, description="Provides built in benchmarks, rules and configurations available for use.")

@router.get("/", response_model=list[TenantOutput])
def get_tenants(session: Session = Depends(get_session)) -> list[TenantOutput]:
    tenants = session.exec(select(Tenant)).all()
    return tenants

@router.post("/", response_model=TenantOutput)
def add_tenant(tenant_name: str, session: Session = Depends(get_session)) -> TenantOutput:
    new_tenant = Tenant(name=tenant_name)
    session.add(new_tenant)
    session.commit()
    session.refresh(new_tenant)
    return new_tenant

@router.get("/{tenant_id}", response_model=TenantOutput)
def get_tenant(tenant_id: int, session: Session = Depends(get_session)) -> TenantOutput:
    tenant = session.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant
