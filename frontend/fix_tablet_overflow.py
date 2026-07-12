import os

files_to_fix = [
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\students.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\timetable.html"
]

for path in files_to_fix:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to change the responsive breakpoints from sm to xl/lg so it stacks on tablets
    
    # 1. Parent container
    content = content.replace(
        'class="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6"',
        'class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 mb-6"'
    )
    
    # 2. Inner containers (left and right button groups)
    content = content.replace(
        'class="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto"',
        'class="flex flex-col sm:flex-row flex-wrap items-center gap-3 w-full xl:w-auto"'
    )
    content = content.replace(
        'class="flex items-center gap-3 w-full sm:w-auto"',
        'class="flex items-center flex-wrap gap-3 w-full xl:w-auto"'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed tablet overflow in {path}")
