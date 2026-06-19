import os

with open('env.txt', 'r', encoding='utf-16') as f:
    for line in f:
        line = line.strip()
        if line and '=' in line and not line.startswith('RAILWAY_'):
            key, val = line.split('=', 1)
            print(f'Setting {key}...')
            # railway CLI doesn't need --service if we are linked properly, but we'll add it
            os.system(f'railway variables set {key}="{val}" --service jarvis-ax-cloud')
