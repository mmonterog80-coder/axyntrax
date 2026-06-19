import os
import subprocess

with open('C:/AXYNTRAX/.env', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            key, val = line.split('=', 1)
            cmd = f'railway variables set "{key}={val}"'
            print(f'Setting {key}...')
            subprocess.run(cmd, shell=True, cwd='C:/AXYNTRAX')
