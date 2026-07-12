import os

files_to_fix = [
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\students.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\timetable.html"
]

for path in files_to_fix:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Revert the w-full sm:w-auto from the blue buttons
    content = content.replace(
        'class="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-550 hover:scale-[1.02] text-white font-semibold py-2.5 px-6 rounded-xl shadow-md transition-all w-full sm:w-auto"',
        'class="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-550 hover:scale-[1.02] text-white font-semibold py-2.5 px-6 rounded-xl shadow-md transition-all"'
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Reverted full-width button in {path}")
