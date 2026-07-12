import os
import re

frontend_dir = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend"

html_files = []
for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

# 1. Update HTML files
pattern = re.compile(
    r'<div class="h-20 flex items-center px-6 border-b border-slate-800 gap-3 brand-logo-container">\s*'
    r'<i data-lucide="school" class="w-6 h-6 text-blue-400"></i>\s*'
    r'<span class="text-lg font-bold text-white tracking-wider font-outfit brand-text">Smart Campus</span>\s*'
    r'</div>'
)

replacement = """<div class="h-20 flex items-center justify-between px-6 border-b border-slate-800 brand-logo-container w-full">
                    <div class="flex items-center gap-3">
                        <i data-lucide="school" class="w-6 h-6 text-blue-400"></i>
                        <span class="text-lg font-bold text-white tracking-wider font-outfit brand-text">Smart Campus</span>
                    </div>
                    <button class="close-sidebar-btn lg:hidden text-slate-400 hover:text-white transition-colors p-1 rounded-md hover:bg-slate-800 focus:outline-none">
                        <i data-lucide="x" class="w-5 h-5"></i>
                    </button>
                </div>"""

for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = pattern.sub(replacement, content)
    # bump version if needed
    if new_content != content:
        new_content = re.sub(r'utils\.js\?v=\d+', 'utils.js?v=6', new_content)
        new_content = re.sub(r'utils\.js"', 'utils.js?v=6"', new_content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added X button to {path}")

# 2. Update utils.js
utils_path = os.path.join(frontend_dir, "js", "utils.js")
with open(utils_path, 'r', encoding='utf-8') as f:
    utils_content = f.read()

if ".close-sidebar-btn" not in utils_content:
    js_injection = """
    const closeBtns = document.querySelectorAll('.close-sidebar-btn');
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (sidebar) {
                sidebar.classList.add('-translate-x-full');
                sidebar.style.transform = '';
            }
            if (overlay) {
                overlay.classList.add('hidden');
            }
        });
    });
"""
    # Insert it right before the end of DOMContentLoaded block
    utils_content = utils_content.replace(
        "    if (overlay) {",
        js_injection + "\n    if (overlay) {"
    )
    with open(utils_path, 'w', encoding='utf-8') as f:
        f.write(utils_content)
    print("Updated utils.js with close button listener")
