import pygame
import sys
import math
import requests
import psutil
from datetime import datetime
from dotenv import load_dotenv
import os
import threading
import time

load_dotenv(dotenv_path=r"C:\AXYNTRAX\.env")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8000")

# ConfiguraciÃ³n de pantalla
WIDTH, HEIGHT = 1024, 768
BG_COLOR = (5, 5, 15)
RING_COLOR = (0, 180, 220)
TEXT_COLOR = (200, 220, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("JARVIS AX - AXYNTRAX Automation Suite")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

# Estado interno
user_input = ""
console_lines = []
angle_outer = 0
angle_inner = 0

orchestrator_status = False

def poll_orchestrator():
    global orchestrator_status
    while True:
        try:
            r = requests.get(f"{ORCHESTRATOR_URL}/health", timeout=2)
            orchestrator_status = (r.status_code == 200)
        except:
            orchestrator_status = False
        time.sleep(2)

threading.Thread(target=poll_orchestrator, daemon=True).start()

def check_orchestrator():
    return orchestrator_status

def send_task(command):
    try:
        import uuid
        payload = {
            "session_id": str(uuid.uuid4()),
            "origin": "hud_jarvis",
            "task": {
                "phase": 1,
                "module": "hud",
                "action_type": "execute",
                "objective": command,
                "context": {
                    "model_preference": "deepseek-coder",
                    "files_allowed": [],
                    "risk_level": "low"
                }
            }
        }
        r = requests.post(f"{ORCHESTRATOR_URL}/tasks", json=payload, timeout=5)
        if r.status_code == 201:
            data = r.json()
            return f"[{data.get('status', '?')}] {data.get('plan', 'Sin plan')}"
        return f"Error {r.status_code}"
    except Exception as e:
        return f"Sin conexiÃ³n: {e}"

def draw_background(screen):
    cx, cy = screen.get_width()//2, screen.get_height()//2
    max_r = max(screen.get_width(), screen.get_height())//2
    for r in range(0, max_r, 6):
        color = (5 + r//15, 5 + r//15, 15 + r//10)
        pygame.draw.circle(screen, color, (cx, cy), r)

def draw_rings(screen):
    global angle_outer, angle_inner
    cx, cy = screen.get_width()//2, screen.get_height()//2
    radius_outer = 180
    radius_inner = 110
    for i in range(36):
        a = math.radians(i*10 + angle_outer)
        x = cx + radius_outer * math.cos(a)
        y = cy + radius_outer * math.sin(a)
        pygame.draw.circle(screen, RING_COLOR, (int(x), int(y)), 3)
    for i in range(24):
        a = math.radians(i*15 - angle_inner)
        x = cx + radius_inner * math.cos(a)
        y = cy + radius_inner * math.sin(a)
        pygame.draw.circle(screen, (0, 220, 255), (int(x), int(y)), 2)
    angle_outer = (angle_outer + 1) % 360
    angle_inner = (angle_inner - 1.5) % 360

def draw_hud(screen):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    orch = "ON" if check_orchestrator() else "OFF"
    lines = [
        f"CPU: {cpu}%",
        f"RAM: {ram}%",
        f"Hora: {datetime.now().strftime('%H:%M:%S')}",
        f"Orquestador: {orch}",
        "> Escribe tu orden y presiona ENTER"
    ]
    y = 15
    for line in lines:
        surf = font.render(line, True, TEXT_COLOR)
        screen.blit(surf, (20, y))
        y += 25

def draw_console(screen):
    y = screen.get_height() - 180
    for line in console_lines[-12:]:
        surf = font.render(line, True, (180, 200, 255))
        screen.blit(surf, (20, y))
        y += 22

def draw_input(screen):
    prompt = "> " + user_input
    surf = font.render(prompt, True, (255, 255, 255))
    screen.blit(surf, (20, screen.get_height() - 45))

def main():
    global user_input, console_lines, screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.strip():
                        console_lines.append(f">> {user_input}")
                        
                        def process_task_bg(cmd):
                            resp = send_task(cmd)
                            console_lines.append(resp)
                            import sys
                            if r"C:\AXYNTRAX\backend\jarvis_orchestrator" not in sys.path:
                                sys.path.append(r"C:\AXYNTRAX\backend\jarvis_orchestrator")
                            try:
                                generar_y_reproducir(resp)
                            except Exception as e:
                                print("Error voz:", e)
                                
                        threading.Thread(target=process_task_bg, args=(user_input,), daemon=True).start()
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        draw_background(screen)
        draw_rings(screen)
        draw_hud(screen)
        draw_console(screen)
        draw_input(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
