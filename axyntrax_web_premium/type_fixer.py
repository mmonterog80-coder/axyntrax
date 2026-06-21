import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find component definitions like:
    # const ComponentName = ({ prop1, prop2, className }) => {
    # and replace with:
    # const ComponentName = ({ prop1, prop2, className }: { prop1?: any, prop2?: any, className?: string, children?: React.ReactNode }) => {
    
    # We will just suppress implicitly any errors by adding `any` to parameters that don't have types in destructured objects
    
    def repl(match):
        inner = match.group(2)
        if ':' in inner: # Already has types
            return match.group(0)
        
        props = [p.strip() for p in inner.split(',')]
        type_defs = []
        for p in props:
            if not p: continue
            if '=' in p:
                p_name = p.split('=')[0].strip()
            else:
                p_name = p
            
            if p_name == 'children':
                type_defs.append('children?: React.ReactNode')
            elif p_name == 'className':
                type_defs.append('className?: string')
            else:
                type_defs.append(f'{p_name}?: any')
        
        types_str = '{ ' + ', '.join(type_defs) + ' }'
        return f"{match.group(1)}({{ {inner} }}: {types_str})"
        
    # Match: const Component = ({ a, b }) =>
    new_content = re.sub(r'(const\s+[A-Za-z0-9_]+\s*=\s*)\(\{\s*([^}]+)\s*\}\)', repl, content)
    # Match: function Component({ a, b }) {
    new_content = re.sub(r'(function\s+[A-Za-z0-9_]+\s*)\(\{\s*([^}]+)\s*\}\)', repl, new_content)
    
    if new_content != content:
        # ensure React is imported if ReactNode is used
        if 'ReactNode' in new_content and 'import React' not in new_content:
            new_content = 'import React from "react";\n' + new_content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            process_file(os.path.join(root, file))
