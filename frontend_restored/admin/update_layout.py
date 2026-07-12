import re

with open(r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html', 'r', encoding='utf-8') as f:
    fac_html = f.read()

with open(r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\students.html', 'r', encoding='utf-8') as f:
    stu_html = f.read()

head_match = re.search(r'(?s)(.*?<!-- Page Content -->)', fac_html)
new_head = head_match.group(1)

new_head = new_head.replace('<title>Faculty - Smart Campus</title>', '<title>Students - Smart Campus</title>')
new_head = new_head.replace('Faculty Management', 'Student Management')

inactive_class = 'flex items-center gap-3 px-4 py-3 rounded-lg text-slate-200 hover:bg-slate-800 hover:text-white transition-all font-medium sidebar-item-link'
active_class = 'flex items-center gap-3 px-4 py-3 rounded-lg text-white bg-blue-600 shadow-md shadow-blue-600/20 font-medium sidebar-item-link'

new_head = new_head.replace(f'<a href="faculty.html" class="{active_class}">', f'<a href="faculty.html" class="{inactive_class}">')
new_head = new_head.replace(f'<a href="students.html" class="{inactive_class}">', f'<a href="students.html" class="{active_class} pointer-events-none">')

stu_match = re.search(r'(?s)<!-- Page Content -->(.*)', stu_html)
new_body = stu_match.group(1)

final_html = new_head + '\n<!-- Page Content -->' + new_body

with open(r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\students.html', 'w', encoding='utf-8') as f:
    f.write(final_html)
print('Done!')
