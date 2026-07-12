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
    
    # Revert IIFE endings
    content = content.replace("})();\n    </script>", "});\n    </script>")
    
    # Replace IIFE starts with turbo:load
    content = content.replace("(async () => {", "document.addEventListener('turbo:load', async () => {")
    content = content.replace("(() => {", "document.addEventListener('turbo:load', () => {")

    # In case there were any original DOMContentLoaded that were missed, replace them too
    content = content.replace("document.addEventListener('DOMContentLoaded',", "document.addEventListener('turbo:load',")
            
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {path}")
