from sqlmodel import SQLModel, Field, Relationship
from ..schemas.scan_policies import ResultDataInput

class ResultData(ResultDataInput, table=True):
    __tablename__="results_data"
    id : int = Field(primary_key = True, default=None)
    scan_id = Field(foreign_key="scans.id") # check Ondelete 
    policy_id = Field(foreign_key="policies.id") # check Ondelete
    rule_id = Field(foreign_key="rules.id") # check Ondelete




# The purpose is to make database for each rule result

    
