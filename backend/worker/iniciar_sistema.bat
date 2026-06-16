@echo off
start "JARVIS WORKER" cmd /k "python worker_local.py"
start "ARQUITECTO AUTONOMO" cmd /k "python arquitecto_autonomo.py"
