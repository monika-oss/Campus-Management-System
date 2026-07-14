import os
import re

directories = [
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\admin",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\faculty",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\faculty",
]

overlay_admin = '<div id="adminSidebarOverlay" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 hidden lg:hidden"></div>'
overlay_faculty = '<div id="facultySidebarOverlay" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 hidden lg:hidden"></div>'

for directory in directories:
    if not os.path.exists(directory):
        continue
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False

            # 1. Fix Admin Sidebar
            if 'id="adminSidebar"' in content:
                # Add inset-y-0 left-0 to aside classes
                old_aside_class = 'fixed lg:static h-screen transform -translate-x-full lg:translate-x-0 transition-transform duration-300'
                new_aside_class = 'fixed inset-y-0 left-0 lg:static h-screen transform -translate-x-full lg:translate-x-0 transition-transform duration-300'
                if old_aside_class in content:
                    content = content.replace(old_aside_class, new_aside_class)
                    modified = True
                
                # Insert overlay before the <aside if not already present
                if 'id="adminSidebarOverlay"' not in content:
                    # Find the <aside id="adminSidebar" ... tag
                    aside_pattern = r'(<aside[^>]*id="adminSidebar"[^>]*>)'
                    match = re.search(aside_pattern, content)
                    if match:
                        full_tag = match.group(1)
                        content = content.replace(full_tag, overlay_admin + '\n        ' + full_tag)
                        modified = True

            # 2. Fix Faculty Sidebar
            if 'id="facultySidebar"' in content:
                # Add inset-y-0 left-0 to aside classes
                old_aside_class = 'fixed lg:static h-screen transform -translate-x-full lg:translate-x-0 transition-transform duration-300'
                new_aside_class = 'fixed inset-y-0 left-0 lg:static h-screen transform -translate-x-full lg:translate-x-0 transition-transform duration-300'
                if old_aside_class in content:
                    content = content.replace(old_aside_class, new_aside_class)
                    modified = True
                
                # Insert overlay before the <aside if not already present
                if 'id="facultySidebarOverlay"' not in content:
                    # Clean up old bad overlay names if any (like id="sidebarOverlay")
                    if 'id="sidebarOverlay"' in content:
                        content = content.replace('id="sidebarOverlay"', 'id="facultySidebarOverlay"')
                        modified = True
                    else:
                        aside_pattern = r'(<aside[^>]*id="facultySidebar"[^>]*>)'
                        match = re.search(aside_pattern, content)
                        if match:
                            full_tag = match.group(1)
                            content = content.replace(full_tag, overlay_faculty + '\n        ' + full_tag)
                            modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed sidebar in {directory}\\{filename}")
