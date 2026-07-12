import re
import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Employee ID to Add Faculty Modal
add_emp_field = '''<div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Employee ID</label>
                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="f_emp" placeholder="Auto-generated if left blank">
                    </div>
                    <div>'''
if 'id="f_emp"' not in content:
    content = content.replace('<div>\n                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Department*</label>', add_emp_field + '\n                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Department*</label>')

# 2. Add Employee ID to Edit Faculty Modal
edit_emp_field = '''<div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Employee ID</label>
                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="ef_emp">
                    </div>
                    <div>'''
if 'id="ef_emp"' not in content:
    content = content.replace('<div>\n                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Department*</label>', edit_emp_field + '\n                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Department*</label>', 1)
    # The replacement above might fail if it replaces the wrong occurrence or if there are multiple. 
    # Let's use a more robust replacement for the Edit modal by looking for ef_email's parent div.
    
    # Let's re-read and use regex
    pass

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Better replacement for Add Faculty
if 'id="f_emp"' not in content:
    content = re.sub(
        r'(<input type="email".*?id="f_email".*?</div>)',
        r'\1\n                    <div>\n                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Employee ID</label>\n                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="f_emp" placeholder="Auto-generated if blank">\n                    </div>',
        content,
        count=1
    )

# Better replacement for Edit Faculty
if 'id="ef_emp"' not in content:
    content = re.sub(
        r'(<input type="email".*?id="ef_email".*?</div>)',
        r'\1\n                    <div>\n                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Employee ID</label>\n                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="ef_emp">\n                    </div>',
        content,
        count=1
    )

# Update Add payload
if "employee_id: document.getElementById('f_emp').value" not in content:
    content = content.replace(
        "name: document.getElementById('f_name').value,",
        "name: document.getElementById('f_name').value,\n                    employee_id: document.getElementById('f_emp').value,"
    )

# Update Edit modal population
if "document.getElementById('ef_emp').value = f.employee_id;" not in content:
    content = content.replace(
        "document.getElementById('ef_name').value = f.name;",
        "document.getElementById('ef_name').value = f.name;\n                document.getElementById('ef_emp').value = f.employee_id;"
    )

# Update Edit payload
if "employee_id: document.getElementById('ef_emp').value" not in content:
    content = content.replace(
        "name: document.getElementById('ef_name').value,",
        "name: document.getElementById('ef_name').value,\n                employee_id: document.getElementById('ef_emp').value,"
    )

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated faculty.html with Employee ID fields')
