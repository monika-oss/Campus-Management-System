import os

admin_faculty = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\admin\faculty.html'
admin_students = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\admin\students.html'

# Update Faculty
with open(admin_faculty, 'r', encoding='utf-8') as f:
    html = f.read()

# Add Dept button to faculty if not there, and ensure no wrap
dept_btn = '''<button class="flex items-center justify-center gap-2 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 font-semibold py-1.5 px-3 text-sm rounded-xl shadow-sm transition-all whitespace-nowrap" onclick="utils.showModal('addDeptModal')">
                                <i data-lucide="folder-plus" class="w-4 h-4 shrink-0"></i><span>Dept</span>
                            </button>'''

# Find the button wrapper in faculty and replace
import re

new_html = re.sub(
    r'<div class="flex flex-row flex-wrap items-center gap-2 w-full md:w-auto justify-end self-end mt-2 md:mt-0">\s*<button class="flex items-center justify-center gap-2 bg-emerald-50[^>]*>\s*<i data-lucide="download"[^>]*></i><span>Export</span>\s*</button>\s*<button class="flex items-center justify-center gap-2 bg-blue-600[^>]*>\s*<i data-lucide="plus"[^>]*></i><span>Faculty</span>\s*</button>\s*</div>',
    f'''<div class="flex flex-row flex-nowrap items-center gap-2 w-full md:w-auto justify-end self-end mt-2 md:mt-0 ml-auto">
                            <button class="flex items-center justify-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 hover:bg-emerald-100 font-semibold py-1.5 px-3 text-sm rounded-xl shadow-sm transition-all whitespace-nowrap" onclick="utils.exportTableToCSV('facultyTable', 'faculty_export.csv')">
                                <i data-lucide="download" class="w-4 h-4 shrink-0"></i><span>Export</span>
                            </button>
                            {dept_btn}
                            <button class="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-550 hover:scale-[1.02] text-white font-semibold py-1.5 px-4 text-sm rounded-xl shadow-md transition-all whitespace-nowrap" onclick="utils.showModal('addFacultyModal')">
                                <i data-lucide="plus" class="w-4 h-4 shrink-0"></i><span>Faculty</span>
                            </button>
                        </div>''',
    html
)

with open(admin_faculty, 'w', encoding='utf-8') as f:
    f.write(new_html)


# Update Students
with open(admin_students, 'r', encoding='utf-8') as f:
    html_s = f.read()

new_html_s = re.sub(
    r'<div class="flex flex-row flex-wrap items-center gap-2 w-full md:w-auto justify-end self-end mt-2 md:mt-0">\s*<button class="flex items-center justify-center gap-2 bg-emerald-50[^>]*>\s*<i data-lucide="download"[^>]*></i><span>Export</span>\s*</button>\s*<button class="flex items-center justify-center gap-2 bg-white[^>]*>\s*<i data-lucide="folder-plus"[^>]*></i><span>Dept</span>\s*</button>\s*<button class="flex items-center justify-center gap-2 bg-blue-600[^>]*>\s*<i data-lucide="plus"[^>]*></i><span>Student</span>\s*</button>\s*</div>',
    f'''<div class="flex flex-row flex-nowrap items-center gap-2 w-full md:w-auto justify-end self-end mt-2 md:mt-0 ml-auto">
                        <button class="flex items-center justify-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 hover:bg-emerald-100 font-semibold py-1.5 px-3 text-sm rounded-xl shadow-sm transition-all whitespace-nowrap" onclick="utils.exportTableToCSV('studentsTable', 'students_export.csv')">
                            <i data-lucide="download" class="w-4 h-4 shrink-0"></i><span>Export</span>
                        </button>
                        <button class="flex items-center justify-center gap-2 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 font-semibold py-1.5 px-3 text-sm rounded-xl shadow-sm transition-all whitespace-nowrap" onclick="utils.showModal('addDeptModal')">
                            <i data-lucide="folder-plus" class="w-4 h-4 shrink-0"></i><span>Dept</span>
                        </button>
                        <button class="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-550 hover:scale-[1.02] text-white font-semibold py-1.5 px-4 text-sm rounded-xl shadow-md transition-all whitespace-nowrap" onclick="utils.showModal('addStudentModal')">
                            <i data-lucide="plus" class="w-4 h-4 shrink-0"></i><span>Student</span>
                        </button>
                    </div>''',
    html_s
)

with open(admin_students, 'w', encoding='utf-8') as f:
    f.write(new_html_s)

print("Updates completed.")
