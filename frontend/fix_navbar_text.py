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
    
    # Remove the truncation classes and reduce mobile text size to text-base
    content = content.replace(
        'text-lg sm:text-xl font-extrabold text-slate-800 font-outfit truncate max-w-[130px] sm:max-w-none',
        'text-base sm:text-xl font-extrabold text-slate-800 font-outfit leading-tight'
    )
    
    # Reduce left side gap (hamburger to title)
    # <div class="flex items-center gap-4"> (This could appear multiple times, but the first one inside <header id="topNavbar"> is what we care about)
    # Actually it's easier to just do a precise replace for the topNavbar header block.
    # We can replace gap-4 with gap-2 sm:gap-4
    
    # We can use regex to find the topNavbar and replace gaps inside it.
    def replace_navbar_gaps(match):
        navbar_content = match.group(0)
        navbar_content = navbar_content.replace('gap-4', 'gap-2 sm:gap-4')
        navbar_content = navbar_content.replace('gap-6', 'gap-3 sm:gap-6')
        navbar_content = navbar_content.replace('pl-6', 'pl-3 sm:pl-6')
        # make sure to not replace gaps that are already sm:gap-something if any
        return navbar_content

    # Regex to capture the whole header
    content = re.sub(r'<header[^>]*id="topNavbar"[^>]*>[\s\S]*?</header>', replace_navbar_gaps, content)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed mobile navbar text visibility in {path}")
