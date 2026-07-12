import os
import re

frontend_dir = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend"

html_files = []
for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The garbage left behind is:
    #             // Sidebar Collapsible Toggle
    # );
    #             }
    
    # We will use regex to remove anything from "// Sidebar Collapsible Toggle" 
    # up to the next valid comment or code block like "// GSAP" or "// Load" or "try {"
    
    # Actually, let's just find:
    pattern1 = re.compile(r"// Sidebar Collapsible Toggle\s*\n\s*\);\s*\n\s*\}\s*\n")
    pattern2 = re.compile(r"// Sidebar Collapsible Toggle\s*\n\s*\);\s*\n\s*\}")
    
    # Some files might have different garbage. Let's just remove:
    # \);\n            \}
    
    # A safer regex that removes the broken leftover logic:
    # We know the broken logic is strictly under "// Sidebar Collapsible Toggle"
    # Let's match "// Sidebar Collapsible Toggle" and everything until the next "// "
    
    def replacer(match):
        return ""

    new_content = re.sub(r"// Sidebar Collapsible Toggle[\s\S]*?(?=\s*// |\s*</script>|\s*document\.getElementById)", "", content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed syntax error in {path}")
