import os

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
                
                # Remove self-start md:self-auto from h2 tags only!
                # We can just do a replace, but we only want to affect h2 tags.
                # Find all <h2 ...> and replace self-start md:self-auto with nothing
                
                import re
                new_content = re.sub(
                    r'<h2 class="([^"]*)self-start md:self-auto([^"]*)"\s*>',
                    lambda m: f'<h2 class="{m.group(1)}{m.group(2)}">'.replace('  ', ' '),
                    new_content
                )

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f'Reverted h2 headers in {filepath}')
