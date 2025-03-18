from sqlmodel import SQLModel, Field, Relationship
from ..schemas.scan_endpoints import ScanEndpointInput

class ScanEndpointLink(ScanEndpointInput, table=True):
    __tablename__="scan_endpoints"
    scan_id: int | None  = Field(default= None, foreign_key="scans.id", primary_key=True) # check Ondelete 
    endpoint_id : int | None = Field(default= None, foreign_key="endpoints.id", primary_key=True) # check Ondelete



    




