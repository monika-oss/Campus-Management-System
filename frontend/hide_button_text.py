import os

files_to_fix = [
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\students.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\timetable.html"
]

for path in files_to_fix:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Hide the text inside the primary blue button on mobile so it fits next to the other icons
    content = content.replace(
        '<i data-lucide="plus" class="w-5 h-5"></i><span>Student</span>',
        '<i data-lucide="plus" class="w-5 h-5"></i><span class="hidden sm:inline">Student</span>'
    )
    content = content.replace(
        '<i data-lucide="plus" class="w-5 h-5"></i><span>Faculty</span>',
        '<i data-lucide="plus" class="w-5 h-5"></i><span class="hidden sm:inline">Faculty</span>'
    )
    content = content.replace(
        '<i data-lucide="plus" class="w-5 h-5"></i><span>Timetable</span>',
        '<i data-lucide="plus" class="w-5 h-5"></i><span class="hidden sm:inline">Timetable</span>'
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Hid primary button text on mobile in {path}")
