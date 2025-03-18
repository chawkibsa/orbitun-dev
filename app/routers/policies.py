from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..dependencies import get_session
from ..models.policies import Policy
from ..schemas.policies import PolicyOutput, PolicyInput

router = APIRouter(prefix="/api/policies", tags=["Policies Management"])

@router.get("/", response_model = list[PolicyOutput])
def get_policies(session: Session = Depends(get_session)) -> list[PolicyOutput]:
    policies = session.exec(select(Policy)).all()
    return policies

@router.post("/", response_model = PolicyOutput)
def add_policy (*, policy_input : PolicyInput, session : Session = Depends(get_session)) -> PolicyOutput:
    # Create a policy name
    new_policy = Policy.from_orm(policy_input)
    session.add(new_policy)
    session.commit()
    session.refresh(new_policy)
    return new_policy

@router.get("/{policy_id}", response_model = PolicyOutput)
def get_policy(policy_id : int, session: Session = Depends(get_session)) -> PolicyOutput:
    policy = session.get(Policy, policy_id)
    return policy

@router.put("/{policy_id}", response_model= PolicyInput)
def modif_policy(policy_id : int, new_policy: PolicyInput, session: Session = Depends(get_session)) -> PolicyInput:
    policy = session.get(Policy, policy_id)
    if policy:
        policy.name = new_policy.name
        session.commit()
        session.refresh(policy)
        return policy

@router.delete("/{policy_id}")
def delete_policy(policy_id : int, session: Session = Depends(get_session)):
    policy = session.get(Policy, policy_id)
    if policy:
        session.delete(policy)
        session.commit()

