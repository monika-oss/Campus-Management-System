import os

utils_file = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\js\utils.js"

with open(utils_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the global click listener
js_code = """
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
            // Reset z-index of the parent wrapper
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

if "Global action menu click handler" not in content:
    with open(utils_file, 'a', encoding='utf-8') as f:
        f.write(js_code)
    print("Added action menu click handler to utils.js")
else:
    print("Handler already exists")

# Update cache version in bump_cache.py to ensure the browser loads the new JS
bump_script = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\bump_cache.py"
with open(bump_script, 'r', encoding='utf-8') as f:
    bump_content = f.read()
    
# we will just execute bump_cache.py to bump the version to ?v=6
