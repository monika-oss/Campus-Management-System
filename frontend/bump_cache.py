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
    
    # Bump utils.js and animations.js versions
    content = re.sub(r'utils\.js\?v=\d+', 'utils.js?v=5', content)
    content = re.sub(r'utils\.js"', 'utils.js?v=5"', content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
