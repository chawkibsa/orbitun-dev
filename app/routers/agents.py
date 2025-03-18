from fastapi import APIRouter, Depends, Response
from ..dependencies import get_session
from sqlmodel import Session, select
from ..schemas.agents import AgentInput, AgentOutput
from ..models.agents import Agent
#from ..models.scan_agents_link import ScanAgentLink
from fastapi.responses import StreamingResponse
from pathlib import Path

router = APIRouter(prefix="/api/agents", tags=["Agents Managment"])#, description="Provides built in benchmarks, rules and configurations available for use.")

working_directory = Path(__file__).absolute().parent

@router.get("/", response_model = list[AgentInput])
def get_agents(session: Session = Depends(get_session)) -> list[AgentInput]:
    agents = session.exec(select(Agent)).all()
    return agents

# This API endpoint will allow the user to download the specific agent for his OS
@router.get("/redhat")
async def download_redhat_agent():
    async def read_file ():
        with open(working_directory/'../static/redhat_agent.py', 'rb') as f:
            return f.read()

    filebytes = await read_file()
    return Response( 
    content= filebytes,
    headers = {
        'Content-Disposition': f'attachment;filename=redhat',
        'Content-Type': 'application/octet-stream'
    }
    )

# Register agent data in the database
@router.post("/register", response_model=AgentOutput)
def add_agent (agent_input : AgentInput, session : Session = Depends(get_session)) -> AgentOutput:
    # Create a policy name
    new_agent = Agent.from_orm(agent_input)
    session.add(new_agent)
    session.commit()
    session.refresh(new_agent)
    return new_agent


'''
# DEAD : It was developed when agents were assigned directly to the scan, now with the change to the assignement of endpoints to the scan, no need for this block
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