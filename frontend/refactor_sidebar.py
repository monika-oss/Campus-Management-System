import os
import re

frontend_dir = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend"

# 1. Strip inline logic from all HTML files
html_files = []
for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # We will just remove any line containing sidebarToggle or sidebar.classList in JS block
    # Actually it's safer to use regex to remove the whole block.
    # The block starts with "const sidebar = document.getElementById(" and ends with the overlay click listener.
    
    # Regex to match the block:
    pattern = re.compile(
        r"\s*const sidebar = document\.getElementById\('[^']+'\);\s*"
        r"const toggleBtn = document\.getElementById\('sidebarToggle'\);\s*"
        r"const overlay = document\.getElementById\('[^']+'\);\s*"
        r"if \(sidebar && toggleBtn\) \{[\s\S]*?\}\s*"
        r"if \(overlay\) \{[\s\S]*?\}\s*"
    )
    
    content = pattern.sub("\n", content)
    
    # Also in case it wasn't modified yet:
    old_pattern = re.compile(
        r"\s*// Sidebar Collapsible Toggle\s*"
        r"const sidebar = document\.getElementById\('[^']+'\);\s*"
        r"const toggleBtn = document\.getElementById\('sidebarToggle'\);\s*"
        r"if \(sidebar && toggleBtn\) \{\s*"
        r"toggleBtn\.addEventListener\('click', \(\) => \{\s*"
        r"sidebar\.classList\.toggle\('collapsed-sidebar'\);\s*"
        r"\}\);\s*"
        r"\}"
    )
    content = old_pattern.sub("\n", content)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Stripped inline JS from {path}")

# 2. Append global logic to utils.js
utils_path = os.path.join(frontend_dir, "js", "utils.js")
with open(utils_path, 'r', encoding='utf-8') as f:
    utils_content = f.read()

if "sidebarToggle" not in utils_content:
    injection = """

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('aside');
    let overlay = null;
    if (sidebar) {
        overlay = document.getElementById(sidebar.id + 'Overlay');
    }
    
    if (sidebar && toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            if (window.innerWidth < 1024) {
                sidebar.classList.toggle('-translate-x-full');
                if (!sidebar.classList.contains('-translate-x-full')) sidebar.style.transform = 'translateX(0)';
                else sidebar.style.transform = '';
                if (overlay) overlay.classList.toggle('hidden');
            } else {
                sidebar.classList.toggle('collapsed-sidebar');
            }
        });
    }
    if (overlay) {
        overlay.addEventListener('click', () => {
            if (sidebar) {
                sidebar.classList.add('-translate-x-full');
                sidebar.style.transform = '';
            }
            overlay.classList.add('hidden');
        });
    }
});
"""
    with open(utils_path, 'a', encoding='utf-8') as f:
        f.write(injection)
    print("Appended global sidebar logic to utils.js")
