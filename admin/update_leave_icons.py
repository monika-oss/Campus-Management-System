import re
import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\leave.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bs_cdn = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">'
if 'bootstrap-icons.min.css' not in content:
    content = content.replace('</head>', f'    {bs_cdn}\n</head>')

# Approve button
approve_regex = r'<button class="flex items-center gap-1 p-1 px-2.5 bg-emerald.*?<i data-lucide="check".*?</i> Approve</button>'
def repl_approve(m):
    match_str = m.group(0)
    onclick = re.search(r'onclick="(.*?)"', match_str).group(1)
    return f'<button class="p-1.5 px-2 bg-emerald-50 text-emerald-600 border border-emerald-200 hover:bg-emerald-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="{onclick}" title="Approve"><i class="bi bi-check-circle"></i></button>'

content = re.sub(approve_regex, repl_approve, content)

# Reject button
reject_regex = r'<button class="flex items-center gap-1 p-1 px-2.5 bg-rose.*?<i data-lucide="x".*?</i> Reject</button>'
def repl_reject(m):
    match_str = m.group(0)
    onclick = re.search(r'onclick="(.*?)"', match_str).group(1)
    return f'<button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm ml-2" onclick="{onclick}" title="Reject"><i class="bi bi-x-circle"></i></button>'

content = re.sub(reject_regex, repl_reject, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated leave.html buttons")
