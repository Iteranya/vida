import json
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional, Dict
from data.model import AgentDataClass

# --- The Management Class ---
# This class will handle all the logic for creating, reading, updating, and deleting agents.

class AgentManager:
    """
    Manages a collection of agents stored as individual JSON files in a directory.
    """
    def __init__(self, storage_path: str = "data/agents"):
        """
        Initializes the AgentManager.

        Args:
            storage_path (str): The directory path where agent JSON files are stored.
                                This directory will be created if it doesn't exist.
        """
        self.storage_path = Path(storage_path)
        # Ensure the storage directory exists, creating it if necessary.
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_filepath(self, agent_uuid: str) -> Path:
        """Constructs the full file path for a given agent UUID."""
        return self.storage_path / f"{agent_uuid}.json"

    def save_agent(self, agent: AgentDataClass) -> None:
        """
        Saves an agent's data to its corresponding JSON file.
        This will either create a new file or overwrite an existing one.

        Args:
            agent (AgentDataClass): The agent object to save.
        """
        filepath = self._get_filepath(agent.uuid)
        with open(filepath, 'w', encoding='utf-8') as f:
            # Use asdict to convert the dataclass instance to a dictionary
            # indent=4 makes the JSON file human-readable
            json.dump(asdict(agent), f, indent=4)

    def create_agent(self, name: str, description: str, lore: str, personality: str, instructions: str,
                     metadata: Optional[Dict] = None, functions: Optional[Dict] = None, settings: Optional[Dict] = None) -> AgentDataClass:
        """
        Creates a new agent with a unique UUID, saves it to a file, and returns the object.

        Args:
            name (str): The name of the new agent.
            ... (other agent attributes)

        Returns:
            AgentDataClass: The newly created agent object.
        """
        new_uuid = str(uuid.uuid4())
        agent = AgentDataClass(
            uuid=new_uuid,
            name=name,
            description=description,
            lore=lore,
            personality=personality,
            instructions=instructions,
            metadata=metadata or {},
            functions=functions or {},
            settings=settings or {}
        )
        self.save_agent(agent)
        print(f"Agent '{agent.name}' created with UUID: {agent.uuid}")
        return agent

    def get_agent(self, agent_uuid: str) -> Optional[AgentDataClass]:
        """
        Retrieves a single agent by its UUID from its JSON file.

        Args:
            agent_uuid (str): The UUID of the agent to retrieve.

        Returns:
            Optional[AgentDataClass]: The loaded agent object, or None if the file doesn't exist.
        """
        filepath = self._get_filepath(agent_uuid)
        if not filepath.exists():
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Use ** to unpack the dictionary into the dataclass constructor
            return AgentDataClass(**data)

    def list_agents(self) -> List[AgentDataClass]:
        """
        Lists all agents available in the storage directory.

        Returns:
            List[AgentDataClass]: A list of all loaded agent objects.
        """
        agents = []
        for filepath in self.storage_path.glob("*.json"):
            # The filename without the .json extension is the UUID
            agent_uuid = filepath.stem
            agent = self.get_agent(agent_uuid)
            if agent:
                agents.append(agent)
        return agents

    def delete_agent(self, agent_uuid: str) -> bool:
        """
        Deletes an agent's JSON file.

        Args:
            agent_uuid (str): The UUID of the agent to delete.

        Returns:
            bool: True if the agent was deleted, False if the file did not exist.
        """
        filepath = self._get_filepath(agent_uuid)
        if filepath.exists():
            filepath.unlink()  # Deletes the file
            print(f"Agent with UUID {agent_uuid} deleted.")
            return True
        print(f"Agent with UUID {agent_uuid} not found for deletion.")
        return False