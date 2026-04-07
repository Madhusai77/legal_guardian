from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class State(BaseModel):
    harassment_level: str
    legal_stage: str
    resolution_status: str
    user_stress: float
    steps: int
    history: List[Dict[str, Any]]
    scenario: str
    compliance_score: float = 0.0

class Observation(BaseModel):
    state: State
    message: str
    available_actions: List[str]

class Action(BaseModel):
    action_type: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class StepResult(BaseModel):
    observation: Observation
    reward: float = Field(..., ge=0.0, le=1.0)
    done: bool
    info: Dict[str, Any]