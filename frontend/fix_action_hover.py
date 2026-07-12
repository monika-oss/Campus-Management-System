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
    
    original = content
    
    # Remove hover classes from the action menu
    content = content.replace('group-hover/menu:opacity-100 group-hover/menu:visible', 'action-menu-dropdown')
    content = content.replace('group-hover/menu:scale-100', '')
    
    # Also remove hover:z-50 from the parent just in case
    content = content.replace('group/menu z-10 hover:z-50', 'group/menu z-10')
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Removed hover action menu classes in {path}")
