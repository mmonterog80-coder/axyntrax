import time

class SystemState:
    def __init__(self):
        self.active_project = "Esperando misión del mercado..."
        self.active_ai = "JARVIS"
        self.pc_connected = False
        self.last_pc_ping = 0
        self.cloud_status = "Ocioso"
        self.edge_queue = []
        self.edge_responses = []

    def update_pc_ping(self):
        self.last_pc_ping = time.time()
        self.pc_connected = True

    def is_pc_online(self):
        # Si no hubo ping en los últimos 15 segundos, asumimos desconectada
        if time.time() - self.last_pc_ping > 15:
            self.pc_connected = False
        return self.pc_connected

    def set_activity(self, ai_name, project_desc):
        self.active_ai = ai_name
        self.active_project = project_desc

    def push_edge_command(self, command_dict):
        """Envía un comando JSON a la cola del PC del usuario"""
        self.edge_queue.append(command_dict)

    def pop_edge_command(self):
        if self.edge_queue:
            return self.edge_queue.pop(0)
        return None

    def push_edge_response(self, response_text):
        self.edge_responses.append(response_text)
        
    def get_latest_edge_response(self):
        if self.edge_responses:
            return self.edge_responses.pop(0)
        return None

global_state = SystemState()
