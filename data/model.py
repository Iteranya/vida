from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class AgentDataClass:
    uuid: str
    name: str
    description: str
    lore: str
    personality: str
    instructions: str
    metadata: Dict
    functions: Dict
    settings: Dict