import re
import os

paths = [
    r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\students.html',
    r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html'
]

bs_cdn = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">'

for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add Bootstrap Icons if not present
    if 'bootstrap-icons.min.css' not in content:
        content = content.replace('</head>', f'    {bs_cdn}\n</head>')

    # Regex replace Edit button
    edit_regex = r'<button class="p-1 px-3 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-600 hover:text-white rounded-lg text-xs font-semibold transition-colors mr-2" onclick="openEdit.*?Modal\(\${.*?}\)">✏️ Edit</button>'
    
    def repl_edit(m):
        match_str = m.group(0)
        # Extract the onclick part
        onclick = re.search(r'onclick="(.*?)"', match_str).group(1)
        return f'<button class="p-1.5 px-2 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-600 hover:text-white rounded-lg transition-colors mr-2 shadow-sm" onclick="{onclick}" title="Edit"><i class="bi bi-pencil-square"></i></button>'
        
    content = re.sub(edit_regex, repl_edit, content)

    # Regex replace Delete button
    delete_regex = r'<button class="p-1 px-3 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg text-xs font-semibold transition-colors" onclick="delete.*?\(\${.*?}\)">🗑️ Delete</button>'
    
    def repl_delete(m):
        match_str = m.group(0)
        onclick = re.search(r'onclick="(.*?)"', match_str).group(1)
        return f'<button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="{onclick}" title="Delete"><i class="bi bi-trash"></i></button>'

    content = re.sub(delete_regex, repl_delete, content)

    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Buttons converted to icons!")
