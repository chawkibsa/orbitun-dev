from fastapi import APIRouter, Depends
from ..dependencies import get_session
from sqlmodel import Session, select
from ..schemas.tenants import TenantInput, TenantOutput
from ..models.tenants import Tenant


router = APIRouter(prefix="/api/tenants", tags=["Tenants Management"])#, description="Provides built in benchmarks, rules and configurations available for use.")

# Create a scan
@router.post("/", response_model = TenantOutput)
def create_tenant (tenant_input : TenantInput, session : Session = Depends(get_session)) -> TenantOutput:
    # Create a tenant name
    new_tenant = Tenant.from_orm(tenant_input)
    session.add(new_tenant)
    session.commit()
    session.refresh(new_tenant)
    return new_tenant
