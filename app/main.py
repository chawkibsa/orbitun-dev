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

app = FastAPI(title="Orbitun", description="""Welcome to the **Orbitun** API documentation**! 
This application provides a robust and scalable solution for managing policies and their associated rules in a secure and efficient manner. Designed with flexibility and enterprise-grade best practices in mind, this API enables administrators and users to define, assign, and customize policies and rules tailored to their specific needs.
### Key Features 
1. **Policy Management**: 
- Create, update, delete, and retrieve policies effortlessly. 
- List all policies with advanced filtering and sorting capabilities. 
- Retrieve detailed information about a specific policy, including its associated rules and variables. 
2. **Rule Assignment and Customization**: 
- Assign predefined rules to policies based on specific use cases. 
- Remove assigned rules from policies as requirements evolve. 
- Update rule variables dynamically to adapt to changing configurations without affecting other policies. 
3. **Predefined Rule Library**: 
- Centralized repository of reusable rules for consistent policy management. 
- Retrieve the full list of predefined rules or query for specific ones. 
4. **Variable Customization**: 
- Customize variables for each rule assigned to a policy, enabling tailored configurations per policy. 
- Easily manage service types, ports, and other rule-specific parameters. 
5. **RESTful API Design**: 
- Resource-based endpoints adhering to modern RESTful API conventions. 
- Support for nested resources like rules within policies. 
- Explicit HTTP methods for Create, Read, Update, and Delete (CRUD) operations. 
6. **Validation and Security**: 
- Input validation through Pydantic schemas to ensure API safety and reliability. 
- Error handling with detailed, user-friendly error messages and appropriate HTTP status codes. 
### Use Cases 
- **Security Compliance**: 
Define and enforce security rules for different environments (e.g., allow SSH, block Telnet). 
- **Custom Policy Configuration**: 
Assign specific rules and variables to policies tailored to unique scenarios. 
- **Centralized Rule Management**: 
Maintain a single source of truth for rules across multiple policies, reducing redundancy and improving consistency. 
### Built with Modern Technology This API leverages the power of: 
- **FastAPI** for its asynchronous, high-performance web framework. 
- **SQLModel** for database modeling and interaction, combining the benefits of SQLAlchemy and Pydantic. 
### Getting Started 
This API is ready to support a wide range of applications, including enterprise-grade systems and small-scale deployments. Whether you're managing security configurations, infrastructure policies, or custom rule-based systems, this API is your solution for structured and reliable management. 
### Extensibility 
The application is designed to be modular and extensible, making it easy to integrate with other services or expand its capabilities as your needs grow. With a focus on clean code and best practices, the API is built to scale with your business requirements. 
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
    uvicorn.run("app.main:app",reload=True)
