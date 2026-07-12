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
    
    # 1. Inject Turbo if not present
    if "hotwired/turbo" not in content:
        content = content.replace("<head>", '<head>\n    <script type="module" src="https://cdn.skypack.dev/@hotwired/turbo"></script>')

    # 2. Replace DOMContentLoaded with IIFE
    if "document.addEventListener('DOMContentLoaded'" in content:
        # Check if async
        if "document.addEventListener('DOMContentLoaded', async () => {" in content:
            content = content.replace("document.addEventListener('DOMContentLoaded', async () => {", "(async () => {")
            # Replace the closing }); at the end of the script
            content = re.sub(r'\}\);\s*</script>', '})();\n    </script>', content)
        elif "document.addEventListener('DOMContentLoaded', () => {" in content:
            content = content.replace("document.addEventListener('DOMContentLoaded', () => {", "(() => {")
            # Replace the closing }); at the end of the script
            content = re.sub(r'\}\);\s*</script>', '})();\n    </script>', content)
            
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")
