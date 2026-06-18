import os
import re

print("Buscando archivos con modelos deepseek...")

backend_dir = "backend"
files_changed = []

for root, dirs, files in os.walk(backend_dir):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                # Reemplazar modelos por deepseek-chat
                content = re.sub(r'["\']deepseek-coder["\']', '"deepseek-chat"', content)
                content = re.sub(r'["\']deepseek-reasoner["\']', '"deepseek-chat"', content)
                content = re.sub(r'["\']deepseek-v3["\']', '"deepseek-chat"', content)
                content = re.sub(r'["\']deepseek-v2["\']', '"deepseek-chat"', content)
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    files_changed.append(filepath)
                    print(f"Corregido: {filepath}")
            except Exception as e:
                print(f"Error en {filepath}: {e}")

if files_changed:
    print(f"\n{len(files_changed)} archivos corregidos")
else:
    print("\nNo se encontraron modelos incorrectos")
