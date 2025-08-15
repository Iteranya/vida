from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict
from fastapi import APIRouter
from pydantic import BaseModel
from data.crud import AgentManager
from data.model import AgentDataClass


router = APIRouter(
    prefix="/characters",
    tags=["Characters"]
)
class AgentBase(BaseModel):
    """Base model with all common agent attributes."""
    name: str = Field(..., example="Nexus")
    description: str = Field(..., example="A helpful AI assistant for data analysis.")
    lore: str = Field(..., example="Created in the labs of Aktiva Institute.")
    personality: str = Field(..., example="Analytical, precise, and friendly.")
    instructions: str = Field(..., example="Always provide data-driven answers. Cite your sources.")
    metadata: Dict = Field(default_factory=dict, example={"version": "1.2"})
    functions: Dict = Field(default_factory=dict, example={"summarize_text": {"enabled": True}})
    settings: Dict = Field(default_factory=dict, example={"response_length": "medium"})

class AgentCreateModel(AgentBase):
    """Model used for creating a new agent. UUID is not required here."""
    pass

class AgentResponseModel(AgentBase):
    """Model for representing an agent in API responses. Includes the UUID."""
    uuid: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    class Config:
        orm_mode = True # Allows the model to be created from ORM objects (like our dataclass)
        
manager = AgentManager()

@router.post("/agents/", response_model=AgentResponseModel, status_code=status.HTTP_201_CREATED, tags=["Agents"])
def create_agent(agent_data: AgentCreateModel):
    """
    Create a new agent.

    The UUID is generated automatically on the server.
    """
    # The Pydantic model's `dict()` method converts it to a dictionary
    # that we can unpack into our manager's create method.
    new_agent = manager.create_agent(**agent_data.dict())
    return new_agent

@router.get("/agents/", response_model=List[AgentResponseModel], tags=["Agents"])
def list_agents():
    """
    Retrieve a list of all available agents.
    """
    return manager.list_agents()

@router.get("/agents/{agent_uuid}", response_model=AgentResponseModel, tags=["Agents"])
def get_agent(agent_uuid: str):
    """
    Retrieve a single agent by its UUID.
    """
    agent = manager.get_agent(agent_uuid)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with UUID {agent_uuid} not found"
        )
    return agent

@router.put("/agents/{agent_uuid}", response_model=AgentResponseModel, tags=["Agents"])
def update_agent(agent_uuid: str, agent_data: AgentCreateModel):
    """
    Update an existing agent's data.

    This performs a full replacement of the agent's data with the provided payload.
    """
    # First, check if the agent exists to provide a proper 404 error
    if not manager.get_agent(agent_uuid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with UUID {agent_uuid} not found"
        )

    # Create an AgentDataClass instance with the updated data
    updated_agent = AgentDataClass(uuid=agent_uuid, **agent_data.dict())

    # Save the updated agent, overwriting the old file
    manager.save_agent(updated_agent)
    return updated_agent

@router.delete("/agents/{agent_uuid}", status_code=status.HTTP_204_NO_CONTENT, tags=["Agents"])
def delete_agent(agent_uuid: str):
    """
    Delete an agent by its UUID.
    """
    was_deleted = manager.delete_agent(agent_uuid)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with UUID {agent_uuid} not found"
        )
    # A 204 response should have no body, so we return None
    return None