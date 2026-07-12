import os, glob
frontend_dir = r'c:/Users/preet/OneDrive/Desktop/Campus_Management/frontend'
html_files = glob.glob(f'{frontend_dir}/**/*.html', recursive=True)

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = content.replace('class=\
h-16
flex
items-center
px-6
border-b
border-slate-800
gap-3
brand-logo-container\', 'class=\h-20
flex
items-center
px-6
border-b
border-slate-800
gap-3
brand-logo-container\')
    content = content.replace('<header class=\h-16
bg-white/80, <header
class=\h-20 bg-white/80')
    content = content.replace('<header class=\h-16
bg-white
border-b, <header
class=\h-20 bg-white border-b')
    
    if original != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {file}')
