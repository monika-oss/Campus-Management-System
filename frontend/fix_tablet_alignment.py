import os

files_to_fix = [
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\students.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\timetable.html"
]

for path in files_to_fix:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Revert the xl breakpoint back to sm/md, but add flex-wrap and right-alignment
    
    # 1. Parent container
    content = content.replace(
        'class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 mb-6"',
        'class="flex flex-col md:flex-row flex-wrap justify-between items-center gap-4 mb-6"'
    )
    
    # 2. Inner containers (left and right button groups)
    content = content.replace(
        'class="flex flex-col sm:flex-row flex-wrap items-center gap-3 w-full xl:w-auto"',
        'class="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto"'
    )
    
    # 3. Button group (right side)
    # We want to add md:ml-auto and md:justify-end to ensure it stays on the right even if it wraps
    content = content.replace(
        'class="flex items-center flex-wrap gap-3 w-full xl:w-auto"',
        'class="flex items-center flex-wrap gap-3 w-full md:w-auto md:ml-auto md:justify-end"'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed tablet right-alignment in {path}")
