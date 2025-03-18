from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..dependencies import get_session
from ..schemas.rules import RuleOutput
from ..schemas.defaults import DefaultRuleSC, DefaultVariableSC
from ..schemas.variables import VariableOutput
from ..models.policies import Policy
from ..models.rules import Rule
from ..models.variables import Variable
from ..models.defaults import DefaultRule, DefaultVariable

router = APIRouter(prefix="/api/policies/{policy_id}", tags=["Rules Management"])

@router.post("/rules", response_model=RuleOutput)
def add_rule_to_policy(policy_id : int, rule_name : str, session : Session = Depends(get_session)) -> RuleOutput:
    policy = session.get(Policy, policy_id)
    rule_query = select(DefaultRule).where(DefaultRule.name == rule_name)
    default_rule = session.exec(rule_query).all()
    if policy and default_rule:
        rule = Rule(policy_id=policy_id, name = default_rule[0].name)
        session.add(rule)
        session.commit()
        session.refresh(rule)

        variables_query = select(DefaultVariable).where(DefaultVariable.rule_id == default_rule[0].id)
        default_variables = session.exec(variables_query).all()
        if default_variables: #if the rule has variables execute this , then empty list automatic by the the schema
            for __vars__ in default_variables:
                variables = Variable(rule_id=__vars__.rule_id, variable = __vars__.variable, variable_value = __vars__.variable_value)
                session.add(variables)
                session.commit()
                session.refresh(variables)
        return rule
    else:
        raise HTTPException(status_code=404,detail="Invali ID or Rule Name")

@router.get("/rules", response_model = list[RuleOutput])
def get_policy_rules(policy_id: int, session: Session = Depends(get_session)) -> list[RuleOutput]:
    policy = session.get(Policy, policy_id)
    if policy:
        query = select(Rule).where(Rule.policy_id == policy_id)
        rules = session.exec(query).all()
        return rules

@router.get("/{rule_id}", response_model = RuleOutput)
def get_rule (policy_id: int, rule_id : int, session: Session = Depends(get_session)) -> RuleOutput:
    policy = session.get(Policy, policy_id)
    if policy:
        rule = session.get(Rule, rule_id)
        return rule

@router.post("/{rule_id}", response_model = RuleOutput)
def add_rule (policy_id: int, rule_id : int, session: Session = Depends(get_session)) -> RuleOutput:
    policy = session.get(Policy, policy_id)
    rule = session.get(DefaultRule, rule_id)
    policy_rule = session.get(Rule, rule_id)
    if policy and rule and not policy_rule:
        new_rule = Rule(policy_id=policy_id, name = rule.name)
        session.add(new_rule)
        session.commit()
        session.refresh(new_rule)

        variables_query = select(DefaultVariable).where(DefaultVariable.rule_id == rule.id)
        default_variables = session.exec(variables_query).all()
        if default_variables: #if the rule has variables execute this , then empty list automatic by the the schema
            for __vars__ in default_variables:
                variables = Variable(rule_id=__vars__.rule_id, variable = __vars__.variable, variable_value = __vars__.variable_value)
                session.add(variables)
                session.commit()
                session.refresh(variables)
        return new_rule
    else:
        raise HTTPException(status_code=404,detail="Invali ID or Rule Name")   

@router.delete("/{rule_id}")
def delete_policy(policy_id : int, rule_id: int, session: Session = Depends(get_session)):
    policy = session.get(Policy, policy_id)
    rule = session.get(Rule, rule_id)
    if policy and rule:
        session.delete(rule)
        session.commit()
