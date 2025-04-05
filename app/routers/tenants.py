from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_session
from sqlmodel import Session, select
from ..schemas.tenants import TenantInput, TenantOutput
from ..models.tenants import Tenant
from ..models.policies import Policy  # Import Policy model
from ..models.rules import Rule # Import Rule model
from ..models.variables import Variable # Import Variable model


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

@router.delete("/{tenant_id}")
def delete_tenant(tenant_id: int, session: Session = Depends(get_session)):
    """
    Delete a tenant and all associated policies, rules, and variables.
    """
    tenant = session.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Delete associated variables
    rules = session.exec(select(Rule).where(Rule.policy_id.in_(select(Policy.id).where(Policy.tenant_id == tenant_id)))).all()
    for rule in rules:
        session.exec(select(Variable).where(Variable.rule_id == rule.id)).all()
        for variable in session.exec(select(Variable).where(Variable.rule_id == rule.id)).all():
            session.delete(variable)
    
    # Delete associated rules
    for rule in rules:
        session.delete(rule)

    # Delete associated policies
    policies = session.exec(select(Policy).where(Policy.tenant_id == tenant_id)).all()
    for policy in policies:
        session.delete(policy)

    # Delete the tenant
    session.delete(tenant)
    session.commit()
    return {"message": "Tenant and associated data deleted successfully"}
