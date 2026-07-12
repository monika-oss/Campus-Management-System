import os

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
    
    # 1. Update the toggle click
    content = content.replace(
        "sidebar.classList.toggle('-translate-x-full');",
        "sidebar.classList.toggle('-translate-x-full');\n                        if (!sidebar.classList.contains('-translate-x-full')) sidebar.style.transform = 'translateX(0)';\n                        else sidebar.style.transform = '';"
    )
    
    # 2. Update the overlay click
    content = content.replace(
        "sidebar.classList.add('-translate-x-full');\n                    overlay.classList.add('hidden');",
        "sidebar.classList.add('-translate-x-full');\n                    sidebar.style.transform = '';\n                    overlay.classList.add('hidden');"
    )
            
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed mobile toggle in {path}")
