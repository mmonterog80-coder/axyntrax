import os
from uuid import uuid4
from datetime import datetime
from supabase import create_client, Client
from models import TaskCreate, TaskResponse, RunSnapshot, TaskStatus
from plan_generator import generate_plan

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

def create_task(payload: TaskCreate) -> TaskResponse:
    run_id = uuid4()
    now = datetime.utcnow()
    plan = generate_plan(payload.task.objective, payload.task.module, payload.task.phase, payload.task.action_type)
    task_data = {
        "id": str(run_id),
        "session_id": str(payload.session_id),
        "phase": payload.task.phase,
        "module": payload.task.module,
        "objective": payload.task.objective,
        "risk_level": payload.task.context.risk_level.value,
        "changes_summary": [],
        "files_allowed": payload.task.context.files_allowed,
        "todo_next": [],
        "model_used": payload.task.context.model_preference,
        "plan": plan,
        "started_at": now.isoformat(),
    }
    supabase.table("agent_runs").insert(task_data).execute()

    snapshot = RunSnapshot(
        id=run_id,
        phase=task_data["phase"],
        module=task_data["module"],
        objective=task_data["objective"],
        risk_level=task_data["risk_level"],
        status=TaskStatus.pending,
        changes_summary=task_data["changes_summary"],
        files_allowed=task_data["files_allowed"],
        todo_next=task_data["todo_next"],
        created_at=now,
    )
    return TaskResponse(task_id=run_id, status=TaskStatus.pending, plan=plan, run_snapshot=snapshot)

def get_task(task_id: str) -> TaskResponse | None:
    res = supabase.table("agent_runs").select("*").eq("id", task_id).single().execute()
    if not res.data:
        return None
    data = res.data
    snapshot = RunSnapshot(
        id=data["id"], phase=data["phase"], module=data["module"], objective=data["objective"],
        risk_level=data["risk_level"], status=data.get("result", "pending"),
        changes_summary=data.get("changes_summary", []), files_allowed=data.get("files_allowed", []),
        todo_next=data.get("todo_next", []), created_at=datetime.fromisoformat(data["started_at"]),
    )
    return TaskResponse(task_id=data["id"], status=snapshot.status, plan=data.get("plan"), run_snapshot=snapshot)

def get_next_pending_task() -> TaskResponse | None:
    res = supabase.table("agent_runs").select("*").is_("result", "null").order("started_at").limit(1).execute()
    if not res.data:
        return None
    data = res.data[0]
    supabase.table("agent_runs").update({"result": "running"}).eq("id", data["id"]).execute()
    return get_task(data["id"])

def update_task_status(task_id: str, status: str, result: str = None, error_details: str = None):
    updates = {"result": status}
    if result: updates["result"] = result
    if error_details: updates["error_details"] = error_details
    if status in ("completed", "failed"):
        updates["completed_at"] = datetime.utcnow().isoformat()
    supabase.table("agent_runs").update(updates).eq("id", task_id).execute()
    return get_task(task_id)
