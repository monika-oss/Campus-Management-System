import os
import re

html_path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\timetable.html'
js_path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\js\admin\timetable.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

bs_cdn = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">'
if 'bootstrap-icons.min.css' not in html_content:
    html_content = html_content.replace('</head>', f'    {bs_cdn}\n</head>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace Edit button
old_edit = r'<button class="text-slate-400 hover:text-indigo-600 transition-colors" onclick="editTimetable(.*?)">.*?<i data-lucide="edit-2".*?</i>.*?</button>'
def repl_edit(m):
    onclick_content = m.group(1)
    return f'<button class="p-1.5 px-2 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-600 hover:text-white rounded-lg transition-colors mr-2 shadow-sm" onclick="editTimetable{onclick_content}" title="Edit"><i class="bi bi-pencil-square"></i></button>'

js_content = re.sub(old_edit, repl_edit, js_content, flags=re.DOTALL)

# Replace Delete button
old_delete = r'<button class="text-slate-400 hover:text-red-500 transition-colors" onclick="deleteTimetable\(\${tt\.timetable_id}\)">.*?<i data-lucide="trash-2".*?</i>.*?</button>'
js_content = re.sub(old_delete, '<button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="deleteTimetable(${tt.timetable_id})" title="Delete"><i class="bi bi-trash"></i></button>', js_content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
    
print("Updated timetable.html and timetable.js")
