import os, sys, asyncio, signal, time, requests, re
from pathlib import Path
from dotenv import load_dotenv
from system_tools import SystemTools

load_dotenv(dotenv_path=r"C:\AXYNTRAX\.env")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8000")
WORKER_ID = os.getenv("WORKER_ID", "worker_1")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))

def get_next_task():
    try:
        r = requests.get(f"{ORCHESTRATOR_URL}/tasks/next", timeout=5)
        if r.status_code == 200: return r.json()
    except: pass
    return None

def update_task(task_id, status, result=None, error=None):
    payload = {"status": status}
    if result: payload["result"] = result
    if error: payload["error_details"] = error
    try: requests.patch(f"{ORCHESTRATOR_URL}/tasks/{task_id}/status", params=payload, timeout=5)
    except: pass

async def execute_task(task):
    tid = task['task_id']
    plan = task.get('plan') or ''
    workspace = Path("C:\\AXYNTRAX\\workspace")
    workspace.mkdir(exist_ok=True)

    # 1. Intentar extraer código C++ del plan
    code_match = re.search(r'```(?:cpp|c\+\+)?\s*\n(.*?)```', plan, re.DOTALL | re.IGNORECASE)
    if code_match:
        code = code_match.group(1).strip()
        if not code:
            update_task(tid, "failed", error="El bloque de código C++ está vacío")
            return
        file_path = workspace / f"task_{tid[:8]}.cpp"
        SystemTools.write_file(str(file_path), code)
        out = workspace / f"task_{tid[:8]}.exe"
        compiler = os.getenv("WORKER_COMPILER", "g++")
        ret, out_str, err = await SystemTools.run_cmd(f"{compiler} {file_path} -o {out}", cwd=str(workspace))
        if ret == 0:
            update_task(tid, "completed", result=f"Compilado: {out}")
        else:
            update_task(tid, "failed", error=err)
        return

    # 2. Si no hay código, ¿es un comando ejecutable?
    if plan and not plan.startswith("Aquí") and not plan.startswith("Error") and len(plan) < 500:
        # Ejecutar como comando
        ret, out, err = await SystemTools.run_cmd(plan, cwd=str(workspace))
        if ret == 0:
            update_task(tid, "completed", result=out)
        else:
            update_task(tid, "failed", error=err)
        return

    # 3. Si es solo texto conversacional o un plan no ejecutable
    update_task(tid, "failed", error="El plan no contiene código compilable ni un comando ejecutable. El worker solo procesa código C++ o comandos directos.")

async def main_loop():
    print(f"[WORKER {WORKER_ID}] Escuchando tareas...")
    while True:
        task = get_next_task()
        if task:
            print(f"[WORKER] Tarea recibida: {task['task_id']}")
            await execute_task(task)
        await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    def shutdown(): loop.stop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try: loop.add_signal_handler(sig, shutdown)
        except: pass
    loop.run_until_complete(main_loop())
