import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Add Faculty designation input with select
old_add_desig = '''<input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="f_desig" placeholder="e.g. Assistant Professor">'''
new_add_desig = '''<select class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="f_desig">
                            <option value="">Select Designation</option>
                            <option value="Assistant Professor">Assistant Professor</option>
                            <option value="Associate Professor">Associate Professor</option>
                            <option value="Professor">Professor</option>
                            <option value="HOD">Head of Department (HOD)</option>
                        </select>'''
content = content.replace(old_add_desig, new_add_desig)

# Replace Edit Faculty designation input with select
old_edit_desig = '''<input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="ef_desig">'''
new_edit_desig = '''<select class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="ef_desig">
                            <option value="">Select Designation</option>
                            <option value="Assistant Professor">Assistant Professor</option>
                            <option value="Associate Professor">Associate Professor</option>
                            <option value="Professor">Professor</option>
                            <option value="HOD">Head of Department (HOD)</option>
                        </select>'''
content = content.replace(old_edit_desig, new_edit_desig)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated faculty.html designations to select dropdowns')
