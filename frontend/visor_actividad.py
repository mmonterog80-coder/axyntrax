import tkinter as tk
import os
import time
import threading

LOG_FILE = r"C:\AXYNTRAX\logs\worker.log"

class VisorActividad:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de Actividad AXYNTRAX")
        self.root.geometry("400x200")
        
        # Make the window floating, always on top, and somewhat transparent
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.85)
        self.root.configure(bg="black")
        
        self.label = tk.Label(self.root, text="JARVIS AX - VISOR DE ACTIVIDAD", fg="#00ff88", bg="black", font=("Consolas", 10, "bold"))
        self.label.pack(pady=5)
        
        self.text_area = tk.Text(self.root, bg="black", fg="white", font=("Consolas", 9), wrap=tk.WORD, borderwidth=0)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        
        self.last_size = 0
        self.update_logs()

    def update_logs(self):
        if os.path.exists(LOG_FILE):
            current_size = os.path.getsize(LOG_FILE)
            if current_size > self.last_size:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    f.seek(self.last_size)
                    new_lines = f.read()
                    if new_lines:
                        self.text_area.insert(tk.END, new_lines)
                        self.text_area.see(tk.END)
                self.last_size = current_size
        self.root.after(1000, self.update_logs)

if __name__ == "__main__":
    os.makedirs(r"C:\AXYNTRAX\logs", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("Iniciando Visor de Actividad AXYNTRAX...\n")
            
    root = tk.Tk()
    app = VisorActividad(root)
    root.mainloop()
