from fastapi import APIRouter, Depends
from ..dependencies import get_session
from sqlmodel import Session, select
from ..schemas.scans import ScanInput, ScanOutput
#from ..schemas.agents import AgentBase
from ..schemas.endpoints import EndpointOutput
from ..schemas.policies import PolicyOutput
#from ..models.agents import Agent
from ..models.endpoints import Endpoint
from ..models.scans import Scan
from ..models.policies import Policy
from ..models.scan_endpoints_link import ScanEndpointLink
from ..models.scan_policies_link import ScanPolicyLink
from ..utils.rabbitmq import send_scan_request
import json

router = APIRouter(prefix="/api/scans", tags=["Scans Managment"])#, description="Provides built in benchmarks, rules and configurations available for use.")

# Get all the scans
@router.get("/", response_model = list[ScanOutput])
def get_scans(session: Session = Depends(get_session)) -> list[ScanOutput]:
    scans = session.exec(select(Scan)).all()
    return scans

# Create a scan
@router.post("/", response_model = ScanOutput)
def create_scan (scan_input : ScanInput, session : Session = Depends(get_session)) -> ScanOutput:
    # Create a policy name
    new_scan = Scan.from_orm(scan_input)
    session.add(new_scan)
    session.commit()
    session.refresh(new_scan)
    return new_scan

# Get the policy assigned to the scan (non filterable)
@router.get("/{scan_id}/policies/{policy_id}", response_model=PolicyOutput)
def get_scan_policy(scan_id: int, policy_id: int, session: Session = Depends(get_session)) -> PolicyOutput:
    scan = session.get(Scan, scan_id)
    policy = session.get(Policy, policy_id)
    if scan and policy:
        # Check if the endpoint is already assigned to the scan from the assignment table
        query = select(ScanPolicyLink).where(ScanPolicyLink.scan_id == scan_id, ScanPolicyLink.policy_id == policy_id)
        assigned = session.exec(query).all()
        if assigned:
            return policy

# Assign a policy to a scan 
@router.post("/{scan_id}/policies/{policy_id}", response_model = ScanOutput)
def add_policy_scan(scan_id: int, policy_id: int, session: Session = Depends(get_session)) -> ScanOutput:
    scan = session.get(Scan, scan_id)
    policy = session.get(Policy, policy_id)
    # Check if the scan and policy are available in the database
    if scan and policy:
        # Check if the endpoint is already assigned to the scan from the assignment table
        query = select(ScanPolicyLink).where(ScanPolicyLink.scan_id == scan_id, ScanPolicyLink.policy_id == policy_id)
        assigned = session.exec(query).all()
        if not assigned:
            # The assign that endpoint to that scan
            policy_scan = ScanPolicyLink(scan_id = scan_id, policy_id=policy_id)
            session.add(policy_scan)
            session.commit()
            session.refresh(policy_scan)
            return scan

# Remove a policy from a scan
@router.delete("/{scan_id}/policies/{policy_id}")
def remove_policy_scan(scan_id : int, policy_id: int, session: Session = Depends(get_session)):
    query = select(ScanPolicyLink).where(ScanPolicyLink.scan_id == scan_id, ScanPolicyLink.policy_id == policy_id)
    policy = session.exec(query).all()
    if policy:
        session.delete(policy[0])
        session.commit()
        return {"message": "policy removed from scan"}

# List all endpoint of one scan (filterable)
@router.get("/{scan_id}/endpoints/", response_model= list[EndpointOutput])
def get_endpoints_scan(scan_id: int, session: Session = Depends(get_session)) -> list[EndpointOutput]:
    scan = session.get(Scan, scan_id)
    # if the scan exists, then get all the related endpoints from the link table
    if scan:
        query = select(ScanEndpointLink).where(ScanEndpointLink.scan_id == scan.id)
        endpoints = session.exec(query).all()
        # Get every endpoint id, select from the Endpoint class table and display them as a list
        output = []
        for endpoint in endpoints:
            query = select(endpoint).where(Endpoint.id == endpoint.endpoint_id)
            endpoint_output = session.exec(query).one()
            output.append(endpoint_output)
        return output

# Get one endpoint assigned to the scan (non filterable)
@router.get("/{scan_id}/endpoints/{endpoint_id}", response_model=EndpointOutput)
def get_scan_endpoint(scan_id: int, endpoint_id: int, session: Session = Depends(get_session)) -> EndpointOutput:
    scan = session.get(Scan, scan_id)
    endpoint = session.get(Endpoint, endpoint_id)
    if scan and endpoint:
        # Check if the endpoint is already assigned to the scan from the assignment table
        query = select(ScanEndpointLink).where(ScanEndpointLink.scan_id == scan_id, ScanEndpointLink.policy_id == policy_id)
        assigned = session.exec(query).all()
        if assigned:
            return endpoint

# Assign endpoint to a scan (query param)
@router.post("/{scan_id}/endpoints/{endpoint_id}", response_model=ScanOutput)
def assign_endpoint_scan(scan_id : int, endpoint_id: int, session: Session = Depends(get_session)) -> ScanOutput:
    scan = session.get(Scan, scan_id)
    endpoint = session.get(Endpoint, endpoint_id)
    # Check if the scan and endpoint are available in the database
    if scan and Endpoint:
        # Check if the endpoint is already assigned to the scan from the assignment table
        query = select(ScanEndpointLink).where(ScanEndpointLink.scan_id == scan_id, ScanEndpointLink.endpoint_id == endpoint_id)
        assigned = session.exec(query).all()
        if not assigned:
            # The assign that endpoint to that scan
            endpoint_scan = ScanEndpointLink(scan_id = scan_id, endpoint_id=endpoint_id)
            session.add(endpoint_scan)
            session.commit()
            session.refresh(endpoint_scan)
            return scan

# Remove an endpoint from a scan
@router.delete("/{scan_id}/endpoints/{endpoint_id}")
def remove_endpoint_scan(scan_id : int, endpoint_id: int, session: Session = Depends(get_session)):
    query = select(ScanEndpointLink).where(ScanEndpointLink.scan_id == scan_id, ScanEndpointLink.endpoint_id == endpoint_id)
    endpoint = session.exec(query).all()
    if endpoint:
        session.delete(endpoint[0])
        session.commit()
        return {"message": "policy removed from scan"}


'''
# DORMANT : This API endpoint works fine, unless I decide from a logical approach to assign multiple policies to a scan
# List one policies of one scan (filterable)
@router.get("/{scan_id}/policies", response_model=list[PolicyOutput])
def get_scan_policies(scan_id: int, session: Session = Depends(get_session)) -> list[PolicyOutput]:
    scan = session.get(Scan, scan_id)
    # if the scan exists, then get all the related policies from the link table
    if scan:
        query = select(ScanPolicyLink).where(ScanPolicyLink.scan_id == scan.id)
        policies = session.exec(query).all()
        # Get every endpoint id, select from the Endpoint class table and display them as a list
        output = []
        for policy in policies:
            query = select(Policy).where(Policy.id == policy.policy_id)
            policy_output = session.exec(query).one()
            output.append(policy_output)
        return output
'''

'''
@router.get("/{scan_id}/agents/", response_model= list[AgentBase])
def get_agent_scan(scan_id: int, session: Session = Depends(get_session)) -> list[AgentBase]:
    scan = session.get(Scan, scan_id)
    # if the scan exists, then get all the related agents from the link table
    if scan:
        query = select(ScanEndpointLink).where(ScanEndpointLink.scan_id == scan.id)
        agents = session.exec(query).all()
        # Get every agent id, select from the Agent class table and display them as a list
        output = []
        for agent in agents:
            query = select(Agent).where(Agent.id == agent.agent_id)
            agent_output = session.exec(query).one()
            output.append(agent_output)

        return output
'''

@router.put("/{scan_id}/submit", response_model=ScanOutput)
def submit_scan(scan_id: int, session:Session = Depends(get_session)) -> ScanOutput:
    scan = session.get(Scan, scan_id)
    if scan:
        scan.status = "pending"
        session.commit()
        session.refresh(scan)
        print(type(scan))
        #to json
        jsonscan = ScanOutput.model_validate(scan).model_dump_json() #json.dumps(scan.to_dict())
        # Send scan to queue
        send_scan_request(jsonscan)


        return scan



