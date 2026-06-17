import sys, os, requests, psutil, threading
from PySide6.QtCore import QObject, Signal, Slot, QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path=r"C:\AXYNTRAX\.env")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8000")

class JarvisBackend(QObject):
    def __init__(self):
        super().__init__()
        self._timer = QTimer()
        self._timer.timeout.connect(self.update_system_info)
        self._timer.start(2000)

    cpuChanged = Signal(float)
    ramChanged = Signal(float)
    timeChanged = Signal(str)
    consoleOutput = Signal(str)
    newResponse = Signal(str)

    @Slot()
    def update_system_info(self):
        self.cpuChanged.emit(psutil.cpu_percent())
        self.ramChanged.emit(psutil.virtual_memory().percent)
        self.timeChanged.emit(datetime.now().strftime("%H:%M:%S"))

    @Slot(str)
    def sendCommand(self, command):
        if not command.strip():
            return
        self.consoleOutput.emit(f">> {command}")
        
        def do_request():
            try:
                import uuid
                payload = {
                    "session_id": str(uuid.uuid4()),
                    "origin": "hud_epic",
                    "task": {
                        "phase": 1,
                        "module": "hud",
                        "action_type": "execute",
                        "objective": command,
                        "context": {"model_preference": "deepseek-coder", "files_allowed": [], "risk_level": "low"}
                    }
                }
                r = requests.post(f"{ORCHESTRATOR_URL}/tasks", json=payload, timeout=30)
                if r.status_code == 201:
                    data = r.json()
                    response = data.get('plan', 'Sin plan')
                    self.newResponse.emit(response)
                    self.consoleOutput.emit(f"[JARVIS]: {response}")
                    try:
                        sys.path.append(r"C:\AXYNTRAX\backend\jarvis_orchestrator")
    pass  # voz eliminada
                    except:
                        pass
                else:
                    self.consoleOutput.emit(f"[Error HTTP {r.status_code}]")
            except Exception as e:
                self.consoleOutput.emit(f"[Error: {e}]")
                
        threading.Thread(target=do_request, daemon=True).start()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = JarvisBackend()
    engine.rootContext().setContextProperty("backend", backend)
    qml_path = os.path.join(os.path.dirname(__file__), "hud_epic.qml")
    engine.load(QUrl.fromLocalFile(qml_path))
    if not engine.rootObjects():
        print("Error: rootObjects vacÃ­o. FallÃ³ la carga del QML.")
        sys.exit(-1)
    print("HUD INICIADO CORRECTAMENTE")
    sys.exit(app.exec())
