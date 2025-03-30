from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..dependencies import get_session
from ..models.policies import Policy
from ..schemas.policies import PolicyOutput, PolicyInput, PolicyUpdate
from ..models.tenants import Tenant
from ..schemas.tenants import TenantOutput



router = APIRouter(prefix="/api/policies", tags=["Policies Management"])

@router.get("/", response_model = list[PolicyOutput])
def get_policies(session: Session = Depends(get_session),tenant_id: int|None = None) -> list[PolicyOutput]:
    """
    Get all policies, optionally filtered by tenant_id.
    """
    if tenant_id:
        policies = session.exec(
            select(Policy).where(Policy.tenant_id == tenant_id)
        ).all()
    else:
        policies = session.exec(select(Policy)).all()
    return policies

@router.post("/", response_model=PolicyOutput)
def add_policy(
    *, policy_input: PolicyInput, session: Session = Depends(get_session)
) -> PolicyOutput:
    """
    Add a new policy.
    """
    tenant = session.get(Tenant, policy_input.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    new_policy = Policy(name=policy_input.name, tenant_id=policy_input.tenant_id)
    session.add(new_policy)
    session.commit()
    session.refresh(new_policy)
    return new_policy

@router.get("/{policy_id}", response_model=PolicyOutput)
def get_policy(policy_id: int, session: Session = Depends(get_session)) -> PolicyOutput:
    """
    Get a policy by ID.
    """
    policy = session.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@router.put("/{policy_id}", response_model=PolicyOutput)
def modify_policy(
    policy_id: int,
    policy_update: PolicyUpdate,
    session: Session = Depends(get_session),
) -> PolicyOutput:
    """
    Modify an existing policy.
    """
    policy = session.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    if policy_update.tenant_id:
        tenant = session.get(Tenant, policy_update.tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        policy.tenant_id = policy_update.tenant_id

    if policy_update.name:
        policy.name = policy_update.name

    session.commit()
    session.refresh(policy)
    return policy

@router.delete("/{policy_id}")
def delete_policy(policy_id: int, session: Session = Depends(get_session)):
    """
    Delete a policy.
    """
    policy = session.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    session.delete(policy)
    session.commit()

