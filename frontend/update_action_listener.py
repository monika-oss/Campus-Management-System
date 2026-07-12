import os
import re

utils_file = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\js\utils.js"

with open(utils_file, 'r', encoding='utf-8') as f:
    content = f.read()

# We will modify the global click handler in utils.js to also set z-50 relative on the TR
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
            // Reset z-index of the parent wrapper and row
            if (menu.parentElement) menu.parentElement.classList.remove('z-50');
            const tr = menu.closest('tr');
            if (tr) tr.classList.remove('relative', 'z-50');
        }
    });

    // If an action button was clicked, toggle its menu
    if (isActionBtn) {
        const menu = btn.nextElementSibling;
        if (menu && menu.classList.contains('action-menu-dropdown')) {
            const tr = menu.closest('tr');
            if (menu.classList.contains('opacity-0')) {
                // Open it
                menu.classList.remove('opacity-0', 'invisible', 'scale-95');
                menu.classList.add('opacity-100', 'visible', 'scale-100');
                if (menu.parentElement) menu.parentElement.classList.add('z-50');
                if (tr) tr.classList.add('relative', 'z-[60]');
            } else {
                // Close it
                menu.classList.add('opacity-0', 'invisible', 'scale-95');
                menu.classList.remove('opacity-100', 'visible', 'scale-100');
                if (menu.parentElement) menu.parentElement.classList.remove('z-50');
                if (tr) tr.classList.remove('relative', 'z-[60]');
            }
        }
    }
});
"""

# Replace the existing block
import re
content = re.sub(r'// Global action menu click handler.*?\}\);\n', new_handler, content, flags=re.DOTALL)

with open(utils_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated utils.js to set high z-index on table rows")

# bump cache
bump_script = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\bump_cache.py"
with open(bump_script, 'r', encoding='utf-8') as f:
    bump_content = f.read()
