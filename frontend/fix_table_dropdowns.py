import os
import re

# 1. Revert utils.js to remove tr.relative
utils_file = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\js\utils.js"
with open(utils_file, 'r', encoding='utf-8') as f:
    content = f.read()

new_handler = """
// Global action menu click handler
document.addEventListener('click', (e) => {
    // Check if clicked element is the three dots button or inside it
    let btn = e.target.closest('button');
    const isActionBtn = btn && btn.querySelector('.bi-three-dots-vertical');
    
    // Close all action dropdowns except the one we just clicked
    document.querySelectorAll('.action-menu-dropdown').forEach(menu => {
        if (!isActionBtn || menu.previousElementSibling !== btn) {
            menu.classList.remove('opacity-100', 'visible', 'scale-100');
            menu.classList.add('opacity-0', 'invisible', 'scale-95');
            if (menu.parentElement) menu.parentElement.classList.remove('z-50');
        }
    });

    // If an action button was clicked, toggle its menu
    if (isActionBtn) {
        const menu = btn.nextElementSibling;
        if (menu && menu.classList.contains('action-menu-dropdown')) {
            if (menu.classList.contains('opacity-0')) {
                // Open it
                menu.classList.remove('opacity-0', 'invisible', 'scale-95');
                menu.classList.add('opacity-100', 'visible', 'scale-100');
                if (menu.parentElement) menu.parentElement.classList.add('z-50');
            } else {
                // Close it
                menu.classList.add('opacity-0', 'invisible', 'scale-95');
                menu.classList.remove('opacity-100', 'visible', 'scale-100');
                if (menu.parentElement) menu.parentElement.classList.remove('z-50');
            }
        }
    }
});
"""

content = re.sub(r'// Global action menu click handler.*?\}\);\n', new_handler, content, flags=re.DOTALL)
with open(utils_file, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Fix html files to always open dropdowns downwards
files_to_fix = [
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\students.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\timetable.html",
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\faculty\students.html", # if exists
    r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\faculty\results.html" # if exists
]

for path in files_to_fix:
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Replace the dynamic dropdownClasses logic
    html_content = html_content.replace(
        "const isLastRows = index >= paginated.length - 2 && paginated.length > 2;\n                    const dropdownClasses = isLastRows ? 'bottom-full mb-1 origin-bottom-right' : 'mt-1 origin-top-right';",
        "const dropdownClasses = 'mt-1 origin-top-right';"
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_content)

print("Fixed row rendering bug and dropdown direction")
