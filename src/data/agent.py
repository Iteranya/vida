import json
from pathlib import Path
from typing import Dict, Any
from contextlib import contextmanager
from data.const import AGENT_PATH

class AgentConfigManager:
    """Simple, elegant manager for agent JSON configurations"""
    
    def __init__(self, base_path: str = AGENT_PATH):
        self.base_path = Path(base_path)
    
    def load_json(self, agent_id: str, filename: str) -> Dict[str, Any]:
        """Load a JSON file for an agent"""
        file_path = self.base_path / agent_id / filename
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_json(self, agent_id: str, filename: str, data: Dict[str, Any]) -> None:
        """Save data to a JSON file for an agent"""
        file_path = self.base_path / agent_id / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @contextmanager
    def agent_context(self, agent_id: str):
        """Context manager for working with a specific agent"""
        yield AgentContext(self, agent_id)

class AgentContext:
    """Simple context for agent operations"""
    
    def __init__(self, manager: AgentConfigManager, agent_id: str):
        self.manager = manager
        self.agent_id = agent_id
    
    def __getitem__(self, filename: str) -> Dict[str, Any]:
        return self.manager.load_json(self.agent_id, filename)
    
    def __setitem__(self, filename: str, data: Dict[str, Any]) -> None:
        self.manager.save_json(self.agent_id, filename, data)
    
    @property
    def config(self) -> Dict[str, Any]:
        return self.manager.load_json(self.agent_id, "config.json")
    
    @config.setter
    def config(self, data: Dict[str, Any]) -> None:
        self.manager.save_json(self.agent_id, "config.json", data)
    
    @property  
    def persona(self) -> Dict[str, Any]:
        return self.manager.load_json(self.agent_id, "persona.json")
    
    @persona.setter
    def persona(self, data: Dict[str, Any]) -> None:
        self.manager.save_json(self.agent_id, "persona.json", data)
    
    @property
    def functions(self) -> Dict[str, Any]:
        return self.manager.load_json(self.agent_id, "functions.json")
    
    @functions.setter
    def functions(self, data: Dict[str, Any]) -> None:
        self.manager.save_json(self.agent_id, "functions.json", data)