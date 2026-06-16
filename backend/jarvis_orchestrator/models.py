from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class TaskContext(BaseModel):
    model_preference: Optional[str] = "deepseek-r1"
    files_allowed: Optional[List[str]] = []
    risk_level: Optional[RiskLevel] = RiskLevel.medium
    require_admin: Optional[bool] = False

class TaskInner(BaseModel):
    phase: int
    module: str
    action_type: str
    objective: str
    context: Optional[TaskContext] = TaskContext()

class TaskCreate(BaseModel):
    session_id: UUID
    origin: str
    task: TaskInner
    preferred_api: Optional[str] = None  # IA preferida (deepseek, kimi, qwen, etc.)

class RunSnapshot(BaseModel):
    id: UUID
    phase: int
    module: str
    objective: str
    risk_level: RiskLevel
    status: TaskStatus
    changes_summary: Optional[List[str]] = []
    files_allowed: Optional[List[str]] = []
    todo_next: Optional[List[str]] = []
    created_at: Optional[datetime] = None

class TaskResponse(BaseModel):
    task_id: UUID
    status: TaskStatus
    plan: Optional[str] = None
    run_snapshot: Optional[RunSnapshot] = None
