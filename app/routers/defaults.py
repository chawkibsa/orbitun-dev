from fastapi import APIRouter, Depends
from ..dependencies import get_session
from sqlmodel import Session, select
from ..schemas.defaults import DefaultRuleSC
from ..models.defaults import DefaultRule


router = APIRouter(prefix="/api/defaults", tags=["defaults"])#, description="Provides built in benchmarks, rules and configurations available for use.")


@router.get("/", response_model = list[DefaultRuleSC])
def get_predefined_rules(session: Session = Depends(get_session)) -> list[DefaultRuleSC]:
    default_rules = session.exec(select(DefaultRule)).all()
    return default_rules
