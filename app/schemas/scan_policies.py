from sqlmodel import SQLModel

class ScanPolicyInput(SQLModel):
    scan_id: int
    policy_id: int

class ScanPolicyOutput(ScanPolicyInput):
    id: int

