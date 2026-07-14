import os, re

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
                
                # Replace left/start alignments with right/end alignment for button wrappers
                new_content = re.sub(r'class="([^"]*)justify-start md:justify-end([^"]*)"', r'class="\1justify-end\2"', new_content)
                
                # For the button container
                new_content = new_content.replace(
                    'class="flex flex-row flex-wrap items-center gap-2 w-full md:w-auto justify-end"',
                    'class="flex flex-row flex-wrap items-center gap-2 w-full md:w-auto justify-end self-end mt-2 md:mt-0"'
                )
                
                new_content = new_content.replace(
                    'class="flex flex-col sm:flex-row items-center gap-2 w-full md:w-auto justify-end"',
                    'class="flex flex-col sm:flex-row items-center gap-2 w-full md:w-auto justify-end self-end mt-2 md:mt-0"'
                )

                # For timetable.html button
                new_content = new_content.replace(
                    '<button class="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-550 hover:scale-[1.02] text-white font-semibold py-1.5 px-4 text-sm rounded-xl shadow-md transition-all" onclick="openAddModal()">',
                    '<button class="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-550 hover:scale-[1.02] text-white font-semibold py-1.5 px-4 text-sm rounded-xl shadow-md transition-all self-end md:self-auto mt-2 md:mt-0" onclick="openAddModal()">'
                )

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f'Updated {filepath}')
