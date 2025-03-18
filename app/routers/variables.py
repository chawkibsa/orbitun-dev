from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..dependencies import get_session
from ..schemas.variables import VariableOutput
from ..models.variables import Variable
from ..models.rules import Rule


router = APIRouter(prefix="/api/policies/{policy_id}/rules/{rules_id}/variables", tags=["Variables Management"])


@router.get("/variables", response_model=list[VariableOutput])
def get_variables(policy_id : int, rule_id: int , session: Session = Depends(get_session)) -> list[VariableOutput]:
    query = select(Rule).where(Rule.policy_id == policy_id , Rule.id == id)
    rule_matches = session.exec(query).all()
    if rule_matches:
        query = select(Variable).where(Variable.rule_id == rule_id)
        variables = session.exec(query).all()
        return variables


@router.put("/{variable_id}", response_model=VariableOutput)
def get_variables(policy_id : int, rule_id: int ,variable_id :int, new_variable_value: str, session: Session = Depends(get_session)) -> VariableOutput:
    query = select(Rule).where(Rule.policy_id == policy_id , Rule.id == rule_id)
    rule_matches = session.exec(query).all()
    if rule_matches:
        query = select(Variable).where(Variable.rule_id == rule_matches[0].id, Variable.id == variable_id)
        variables_matches= session.exec(query).all()
        if variables_matches:
            variable = session.get(Variable, variable_id)
            query = select(Variable).where(Variable.variable_value == new_variable_value)
            variable_value_matches = session.exec(query).all()
            if not variable_value_matches:
                variable.variable_value = new_variable_value
                session.commit()
                session.refresh(variable)
                return variable
