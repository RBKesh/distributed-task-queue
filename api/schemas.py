from pydantic import BaseModel
from typing import Dict, Any, Optional

class TaskRequest(BaseModel):
    task_type: str
    payload: Dict[str, Any]

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any]
