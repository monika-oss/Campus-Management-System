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
    
    # 1. GSAP sidebar issue
    gsap_pattern = r'(gsap\.to\([\'"]#(\w+Sidebar)[\'"],\s*\{\s*duration:\s*[\d\.]+,\s*x:\s*0,\s*ease:\s*[\'"][^\'"]+[\'"]\s*\}\);)'
    
    def repl_gsap(m):
        full_match = m.group(1)
        return f'if (window.innerWidth >= 768) {{ {full_match} }}'

    content = re.sub(gsap_pattern, repl_gsap, content)

    # 2. Also fix animations.js if there is any sidebar GSAP
    
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed GSAP in {path}")
