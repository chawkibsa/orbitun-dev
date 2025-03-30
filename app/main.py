#import pdb; pdb.set_trace()
from fastapi import FastAPI , Depends, HTTPException
import uvicorn
from sqlmodel import SQLModel, create_engine, Session, select
from .schemas.defaults import DefaultRuleSC, DefaultVariableSC
from .models.defaults import DefaultVariable, DefaultRule
from .routers import defaults, policies, rules, variables, agents,endpoints, scans, tenants
from fastapi.staticfiles import StaticFiles
import json
import psycopg2
from dotenv import load_dotenv
import os

app = FastAPI(title="Orbitundev", description="""
## Overview
orbitun-dev is the development release of the orbitun project. It has been released to enable the community to contribute, develop, test, deploy, and improve.

orbitun-dev provides programmatic control over security configurations through exposed APIs that interacts with installed agents (sensors) on endpoints.

It allows administrators and security professionals with real-time monitoring and enforcement of CIS (Center for Internet Security) compliance benchmarks.

## Key Features
- **Automated Security Auditing**: Conducts continuous security assessments based on CIS benchmarks.
- **Remediation & Hardening**: Implements corrective actions to align systems with compliance standards.
- **Agent-Based Architecture**: Deployed sensors interact with a centralized API for security policy enforcement.
- **Real-Time Monitoring**: Provides security teams with insights into system compliance status.
- **API-Driven**: Allows seamless integration with existing security workflows.
- **Cross-Platform Support(furture)**: Planned support for multiple operating systems.
- **ML (future)**: AI-driven analytics for advanced prioritization, anomaly detection and compliance automation.

## Problem It Solves
- Out of the box automated compliance enforcement, with no manual effort.
- Standard security policies across distributed environments.
- Real-time insights into security posture and deviations.
### Try It Out! 
Use the endpoints provided in this documentation to interact with the API and explore its functionality. Each endpoint includes a detailed description, input/output examples, and expected responses to guide your integration. """
, version="1.0.0", swagger_ui_parameters={"defaultModelsExpandDepth": -1} )

# Serve static files (e.g., the telemetry script)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

                                                        
# Database setup                                                                             
load_dotenv()  # Load environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")
                                                           
engine = create_engine(DATABASE_URL, echo=True)

def load_config(file_path: str):
    """Load the rules and variables from a JSON configuration file."""
    with open(file_path, "r") as file:
        return json.load(file)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

    

    # Load configuration from the JSON file
    config = load_config("./app/redhat9_controls.json")

    with Session(engine) as session:
        for rule_data in config.get("rules", []):
            # Check if the rule already exists
            existing_rule = session.exec(
                select(DefaultRule).where(DefaultRule.name == rule_data["name"])
            ).first()

            if not existing_rule:
                # Create a new rule
                new_rule = DefaultRule(name=rule_data["name"], path=rule_data["path"])
                session.add(new_rule)
                session.commit()
                session.refresh(new_rule)

                # Add associated variables
                for variable in rule_data.get("variables", []):
                    session.add(DefaultVariable(
                        rule_id=new_rule.id,
                        variable=variable["name"],
                        variable_value=variable["value"],
                    ))
                session.commit()

app.include_router(defaults.router)
app.include_router(variables.router)
app.include_router(rules.router)
app.include_router(policies.router)
app.include_router(agents.router)
app.include_router(tenants.router)
app.include_router(endpoints.router)
app.include_router(scans.router)


if __name__=="__main__":
    uvicorn.run("app.main:app",host="0.0.0.0",reload=True)
