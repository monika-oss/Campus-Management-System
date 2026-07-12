import os
import re

files_to_update = {
    'attendance.html': ('attendanceTable', 'attendance_export.csv', 'Mark Attendance'),
    'results.html': ('resultsTable', 'results_export.csv', 'Add Result'),
    'leave.html': ('leaveTable', 'leave_requests.csv', 'New Leave Request') 
    # Just generic fallbacks for button text
}

base_dir = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin'

for fname, (table_id, export_name, btn_text) in files_to_update.items():
    path = os.path.join(base_dir, fname)
    if not os.path.exists(path):
        continue
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'utils.exportTableToCSV' in content:
        print(f'{fname} already has export button.')
        continue

    # Find a primary action button like <button ... bg-blue-600 ...>
    # We will look for something like `<button class="flex items-center justify-center gap-2 bg-blue-600` 
    # or similar and prefix it with the export button and wrapper div.
    
    btn_match = re.search(r'(<button[^>]*bg-blue-600[^>]*>.*?<\/button>)', content, flags=re.DOTALL)
    if btn_match:
        original_btn = btn_match.group(1)
        export_btn = f'''<div class="flex items-center gap-3 w-full sm:w-auto">
                            <button class="flex items-center justify-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 hover:bg-emerald-100 font-semibold py-2.5 px-4 rounded-xl shadow-sm transition-all" onclick="utils.exportTableToCSV('{table_id}', '{export_name}')">
                                <i data-lucide="download" class="w-5 h-5"></i><span class="hidden sm:inline">Export</span>
                            </button>
                            {original_btn}
                        </div>'''
        new_content = content.replace(original_btn, export_btn)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Added export to {fname}')
    else:
        print(f'Could not find primary button in {fname}')
