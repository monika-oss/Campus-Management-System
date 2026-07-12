import glob
import re
for f in glob.glob('c:/Users/preet/OneDrive/Desktop/Campus_Management/frontend/**/*.html', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    if '<main class="flex-1 overflow-y-auto p-8"' in content:
        content = re.sub(r'<main class="flex-1 overflow-y-auto p-8"', r'<main class="flex-1 overflow-y-auto p-4 md:p-8"', content)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print("Updated:", f)
