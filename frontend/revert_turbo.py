import os
import re

frontend_dir = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend"

html_files = []
for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove Turbo CDN
    content = content.replace('<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@hotwired/turbo@8.0.4/dist/turbo.es2017-umd.js"></script>', "")
    content = content.replace('<script type="module" src="https://cdn.skypack.dev/@hotwired/turbo"></script>', "")
    
    # Revert turbo:load to DOMContentLoaded
    content = content.replace("document.addEventListener('turbo:load',", "document.addEventListener('DOMContentLoaded',")
            
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Reverted {path}")
