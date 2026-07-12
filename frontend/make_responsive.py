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
    
    # 1. Sidebar Class Replacement
    # Match any aside with id *Sidebar
    sidebar_pattern = r'(<aside[^>]+id="(\w+Sidebar)"[^>]*>)'
    
    def repl_sidebar(m):
        full_match = m.group(1)
        sidebar_id = m.group(2)
        # Check if already modified
        if "fixed inset-y-0" in full_match:
            return full_match
            
        # Replace fixed classes
        new_match = full_match.replace("z-20", "z-[100] fixed inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition-transform duration-300 ease-in-out")
        
        # We need to inject the overlay right before the aside
        overlay = f'<div id="{sidebar_id}Overlay" class="fixed inset-0 bg-slate-900/50 z-[90] hidden md:hidden"></div>\n        '
        return overlay + new_match

    content = re.sub(sidebar_pattern, repl_sidebar, content)

    # 2. Top Navbar padding
    content = content.replace("px-8 shadow-sm\" id=\"topNavbar\"", "px-4 md:px-8 shadow-sm\" id=\"topNavbar\"")

    # 3. Content Block padding
    content = content.replace("p-8 space-y-6", "p-4 md:p-8 space-y-4 md:space-y-6")

    # 4. Tables overflow
    content = content.replace("overflow-hidden overflow-x-auto", "overflow-hidden") # prevent duplicate
    content = content.replace("border border-slate-200 overflow-hidden\"", "border border-slate-200 overflow-hidden overflow-x-auto\"")

    # 5. Grids
    content = content.replace("grid-cols-4 gap-6", "grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6")
    content = content.replace("grid-cols-3 gap-6", "grid-cols-1 md:grid-cols-3 gap-4 md:gap-6")
    content = content.replace("grid-cols-2 gap-6", "grid-cols-1 md:grid-cols-2 gap-4 md:gap-6")

    # 6. JavaScript JS logic
    js_old = """            const sidebar = document.getElementById('adminSidebar');
            const toggleBtn = document.getElementById('sidebarToggle');
            if (sidebar && toggleBtn) {
                toggleBtn.addEventListener('click', () => {
                    sidebar.classList.toggle('collapsed-sidebar');
                });
            }"""
            
    # We don't know the exact ID in every file. It could be adminSidebar, facultySidebar, studentSidebar.
    # Let's use regex to find it.
    js_pattern = re.compile(
        r"const sidebar = document\.getElementById\('(\w+Sidebar)'\);\s*"
        r"const toggleBtn = document\.getElementById\('sidebarToggle'\);\s*"
        r"if \(sidebar && toggleBtn\) \{\s*"
        r"toggleBtn\.addEventListener\('click', \(\) => \{\s*"
        r"sidebar\.classList\.toggle\('collapsed-sidebar'\);\s*"
        r"\}\);\s*"
        r"\}"
    )

    def repl_js(m):
        sidebar_id = m.group(1)
        return f"""const sidebar = document.getElementById('{sidebar_id}');
            const toggleBtn = document.getElementById('sidebarToggle');
            const overlay = document.getElementById('{sidebar_id}Overlay');
            if (sidebar && toggleBtn) {{
                toggleBtn.addEventListener('click', () => {{
                    if (window.innerWidth < 768) {{
                        sidebar.classList.toggle('-translate-x-full');
                        if (overlay) overlay.classList.toggle('hidden');
                    }} else {{
                        sidebar.classList.toggle('collapsed-sidebar');
                    }}
                }});
            }}
            if (overlay) {{
                overlay.addEventListener('click', () => {{
                    sidebar.classList.add('-translate-x-full');
                    overlay.classList.add('hidden');
                }});
            }}"""
            
    content = js_pattern.sub(repl_js, content)
            
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Made responsive {path}")
