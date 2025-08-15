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

@dataclass
class ConfigDataClass:
    default_character: str = "Viel"
    ai_endpoint: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    base_llm: str = "gemini-2.5-pro-exp-03-25"
    temperature: float = 0.5
    auto_cap:int = 0
    ai_key: str = ""
    discord_key: str = ""