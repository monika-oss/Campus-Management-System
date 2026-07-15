import os
import glob
import re

files = glob.glob('student/*.html') + glob.glob('faculty/*.html')

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Fix the close button
    old_close_btn = '''<button class="close-sidebar-btn shrink-0 lg:hidden text-slate-400 hover:text-white transition-colors p-1 rounded-md hover:bg-slate-800 focus:outline-none">
                        <i data-lucide="x" class="w-4 h-4 shrink-0"></i>
                    </button>'''
    new_close_btn = '''<button onclick="this.closest('aside').classList.add('-translate-x-full'); this.closest('aside').style.transform = ''; const ov = document.getElementById(this.closest('aside').id + 'Overlay'); if(ov) ov.classList.add('hidden');" class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 shrink-0 block lg:hidden focus:outline-none"><i data-lucide="x" class="w-4 h-4 shrink-0"></i></button>'''
    
    if old_close_btn in content:
        content = content.replace(old_close_btn, new_close_btn)

    # 2. Fix the JS toggle logic
    js_pattern = re.compile(r'// Sidebar Toggle.*?\}\);?\s*\}', re.DOTALL)
    
    if 'student' in filepath:
        prefix = 'student'
    else:
        prefix = 'faculty'
        
    new_js = f'''// Sidebar Toggle
            const sidebar = document.getElementById('{prefix}Sidebar');
            const overlay = document.getElementById('{prefix}SidebarOverlay');
            const toggleBtn = document.getElementById('sidebarToggle');

            if (toggleBtn && sidebar) {{
                toggleBtn.addEventListener('click', () => {{
                    // On mobile, slide in
                    if (window.innerWidth < 1024) {{
                        sidebar.classList.remove('-translate-x-full');
                        sidebar.style.transform = '';
                        if (overlay) overlay.classList.remove('hidden');
                    }} else {{
                        // On desktop, toggle collapse
                        sidebar.classList.toggle('collapsed-sidebar');
                    }}
                }});
            }}
            if (overlay) {{
                overlay.addEventListener('click', () => {{
                    sidebar.classList.add('-translate-x-full');
                    overlay.classList.add('hidden');
                }});
            }}'''
            
    content = js_pattern.sub(new_js, content)
    
    # 3. Ensure the aside has the correct classes
    # Original: <aside class="w-64 bg-slate-900 border-r border-slate-800 text-slate-200 flex flex-col justify-between flex-shrink-0 z-[100] fixed inset-y-0 left-0 transform -translate-x-full lg:relative lg:translate-x-0 transition-transform duration-300 ease-in-out shadow-xl" id="studentSidebar">
    # Desired:  <aside class="w-64 bg-slate-900 border-r border-slate-800 text-slate-200 flex flex-col justify-between flex-shrink-0 z-[100] shadow-xl fixed inset-y-0 left-0 lg:static h-[100dvh] transform -translate-x-full lg:translate-x-0 transition-transform duration-300" id="...">
    aside_pattern = re.compile(r'(<aside class="[^"]*?z-\[100\] )[^"]*?(" id="(?:student|faculty)Sidebar">)')
    content = aside_pattern.sub(r'\1shadow-xl fixed inset-y-0 left-0 lg:static h-[100dvh] transform -translate-x-full lg:translate-x-0 transition-transform duration-300\2', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Done")
