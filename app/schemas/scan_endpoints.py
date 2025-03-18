from sqlmodel import SQLModel

class ScanEndpointInput(SQLModel):
    scan_id: int
    endpoint_id: int

class ScanEndpointOutput(ScanEndpointInput):
    id: int

