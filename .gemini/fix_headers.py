import os
import re

workspace_dir = r'c:\Users\preet\OneDrive\Desktop\Campus_Management'
target_dirs = ['admin', 'student', 'faculty']

for t_dir in target_dirs:
    full_dir = os.path.join(workspace_dir, t_dir)
    if not os.path.exists(full_dir): continue
    for root, dirs, files in os.walk(full_dir):
        for f in files:
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = content
                
                # Replace the main headers to have self-start on mobile
                # E.g. <h3 class="text-lg font-bold text-slate-850 font-poppins">
                # We can match '<h3 class="text-lg font-bold' and add ' self-start md:self-auto' if not present
                
                # Specifically for Campus Announcements
                new_content = re.sub(
                    r'<h3 class="([^"]*text-lg font-bold[^"]*)"\s*>', 
                    lambda m: f'<h3 class="{m.group(1)} self-start md:self-auto">' if 'self-start' not in m.group(1) else m.group(0), 
                    new_content
                )
                
                # Some are text-xl or text-base
                new_content = re.sub(
                    r'<h2 class="([^"]*text-base sm:text-xl font-extrabold[^"]*)"\s*>', 
                    lambda m: f'<h2 class="{m.group(1)} self-start md:self-auto">' if 'self-start' not in m.group(1) else m.group(0), 
                    new_content
                )

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f'Updated headers in {filepath}')
