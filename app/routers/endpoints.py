from fastapi import APIRouter, Depends
from ..dependencies import get_session
from sqlmodel import Session, select
from ..schemas.endpoints import EndpointInput, EndpointOutput
from ..models.endpoints import Endpoint
from ..models.net_ipv4 import NetIpv4
import json
#from ..models.scan_agents_link import ScanAgentLink

router = APIRouter(prefix="/api/endpoints", tags=["Endpoints Managment"])#, description="Provides built in benchmarks, rules and configurations available for use.")

@router.get("/", response_model = list[EndpointOutput])
def get_endpoints(session: Session = Depends(get_session)) -> list[EndpointOutput]:
    endpoints = session.exec(select(Endpoint)).all()
    return endpoints

@router.post("/register", response_model = EndpointOutput)
def register_endpoint(endpoint_input : EndpointInput, session : Session = Depends(get_session)) -> EndpointOutput:
    # Create a policy name
    #new_endpoint = Endpoint.from_orm(endpoint_input)
    dict_new_endpoint = endpoint_input.dict()
    # The reason I used this method and not from_orm() is that the table is not designed to get the pydantic model as it is, I should parse and extract the metadata such as IPv4, IPv6 ..
    new_endpoint_name = dict_new_endpoint["name"]
    new_endpoint_description = dict_new_endpoint["description"]
    new_endpoint_hostname = dict_new_endpoint["hostname"]
    new_endpoint_device_type = dict_new_endpoint["device_type"]
    new_endpoint_os_type = dict_new_endpoint["os_type"]
    new_endpoint_os_version = dict_new_endpoint["os_version"]
    new_endpoint_created_at = "current creation time" # should be modified to time
    new_endpoint_updated_at = "current updated time"
    new_endpoint = Endpoint(name=new_endpoint_name, description=new_endpoint_description, hostname=new_endpoint_hostname, device_type= new_endpoint_device_type, os_type = new_endpoint_os_type, os_version= new_endpoint_os_version, created_at= new_endpoint_created_at, updated_at= new_endpoint_updated_at)
    # I still need to add the time
    session.add(new_endpoint)
    session.commit()
    session.refresh(new_endpoint)

    for ipv4_addr in dict_new_endpoint["ipv4_addresses"]:
        #print(ipv4_addr["addresse"]) DEAD
        ipv4 = NetIpv4(address=ipv4_addr["address"], endpoint_id=new_endpoint.id )
        session.add(ipv4)
        session.commit()
        session.refresh(ipv4)



    
    #print("\n\n\n")
    #print(type(json_new_endpoint))
    #print(type(endpoint_input))
    #print(type(endpoint_input.dict()))
  

    print("\n\n\n")

    return new_endpoint
    

    #return True
    '''
    session.add(new_endpoint)
    session.commit()
    session.refresh(new_endpoint)
    return new_endpoint
    '''

