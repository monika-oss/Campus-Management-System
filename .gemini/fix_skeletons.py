import os
import re

workspace_dir = r'c:\Users\preet\OneDrive\Desktop\Campus_Management'
html_files = {
    'admin/attendance.html': ('loadAttendance', '#attendanceTable tbody', 6),
    'admin/leave.html': ('loadLeaves', '#leaveTable tbody', 7),
    'admin/results.html': ('loadResults', '#resultsTableBody', 7),
    'admin/announcements.html': ('loadAnnouncements', '#announcementsList', 4) # announcements uses divs, not table maybe? Wait, announcements uses a grid. We'll skip announcements for table skeleton.
}

for file_rel, config in html_files.items():
    filepath = os.path.join(workspace_dir, file_rel)
    if not os.path.exists(filepath): continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    func_name, target, cols = config
    
    # If the function exists and doesn't have showTableSkeleton
    if f'function {func_name}()' in content and 'showTableSkeleton' not in content:
        # inject it right after try { or function body
        new_content = re.sub(
            fr'(async function {func_name}\(\)\s*{{\s*try\s*{{)',
            f'\\1\n                utils.showTableSkeleton(\'{target}\', {cols}, ITEMS_PER_PAGE);',
            content
        )
        if new_content == content:
            new_content = re.sub(
                fr'(function {func_name}\(\)\s*{{\s*try\s*{{)',
                f'\\1\n                utils.showTableSkeleton(\'{target}\', {cols}, ITEMS_PER_PAGE);',
                content
            )
        
        # also we need to make sure the await api.get('/students/departments/') etc doesn't block
        # Look for:
        # const depts = await api.get('/students/departments/');
        # We can wrap the whole block that fetches departments in an IIFE.
        # It's easier to just do it manually with regex if needed, or we just leave the delay for other pages if they are short.
        # But wait, we can just replace `await loadAttendance()` with `loadAttendance()` and remove the await before `api.get` if it's at root level.
        # Let's fix the blocking await calls at root level DOMContentLoaded
        new_content = re.sub(r'await (load\w+\(\));', r'\1;', new_content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_rel}")

