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
    
    # 1. Update the sidebar classes to use lg: instead of md:
    # Before: md:relative md:translate-x-0
    # After: lg:relative lg:translate-x-0
    content = content.replace("md:relative md:translate-x-0", "lg:relative lg:translate-x-0")
    
    # 2. Update the overlay to use lg:hidden instead of md:hidden
    content = content.replace("hidden md:hidden", "hidden lg:hidden")
    
    # 3. Update the GSAP inline if statement
    content = content.replace("if (window.innerWidth >= 768)", "if (window.innerWidth >= 1024)")
    
    # 4. Update the hamburger click JS logic
    content = content.replace("if (window.innerWidth < 768)", "if (window.innerWidth < 1024)")
            
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated breakpoints for {path}")
