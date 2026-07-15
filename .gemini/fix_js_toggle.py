import glob

files = glob.glob('student/*.html') + glob.glob('faculty/*.html')

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
        
    old_toggle = """            if (sidebar && toggleBtn) {
                toggleBtn.addEventListener('click', () => sidebar.classList.toggle('collapsed-sidebar'));
            }"""
            
    new_toggle = """            if (sidebar && toggleBtn) {
                toggleBtn.addEventListener('click', () => {
                    if (window.innerWidth >= 1024) {
                        sidebar.classList.toggle('collapsed-sidebar');
                    }
                });
            }"""
            
    if old_toggle in content:
        content = content.replace(old_toggle, new_toggle)
        print(f"Fixed {filepath}")
        
    with open(filepath, 'w') as f:
        f.write(content)
