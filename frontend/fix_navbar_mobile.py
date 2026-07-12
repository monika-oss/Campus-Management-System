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
    
    # 1. Update the h2 title inside the navbar
    # It usually looks like: <h2 class="text-xl font-extrabold text-slate-800 font-outfit">...</h2>
    # Sometimes it might not have font-outfit or exact classes. Let's use a safe regex.
    content = re.sub(
        r'(<h2 class=")([^"]*)(text-xl[^"]*text-slate-800[^"]*)(">)',
        r'\1\2text-lg sm:\3 truncate max-w-[150px] sm:max-w-none\4',
        content
    )
    
    # Wait, the regex above might be too strict. Let's just do a simple replace on the exact known class string:
    # Most pages use exactly: class="text-xl font-extrabold text-slate-800 font-outfit"
    content = content.replace(
        'class="text-xl font-extrabold text-slate-800 font-outfit"',
        'class="text-lg sm:text-xl font-extrabold text-slate-800 font-outfit truncate max-w-[130px] sm:max-w-none"'
    )
    
    # 2. Update the subtitle paragraph
    # class="text-slate-500 mt-1 text-sm"
    content = content.replace(
        'class="text-slate-500 mt-1 text-sm"',
        'class="hidden sm:block text-slate-500 mt-1 text-sm"'
    )

    # 3. Update the user name span to hide on mobile to save space
    # <span class="font-semibold text-slate-700 text-sm" id="userName">
    content = content.replace(
        'class="font-semibold text-slate-700 text-sm" id="userName"',
        'class="hidden sm:block font-semibold text-slate-700 text-sm" id="userName"'
    )
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed mobile navbar in {path}")
