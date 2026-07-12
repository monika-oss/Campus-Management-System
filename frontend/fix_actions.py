import glob, re

for f in glob.glob('c:/Users/preet/OneDrive/Desktop/Campus_Management/frontend/**/*.html', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original = content
    
    # We want to find the <td class="... text-center ..."> and ensure its buttons are wrapped in a flex container.
    # To do this safely, we will replace `mr-2` on buttons inside the action column.
    
    # Just add whitespace-nowrap to the action td to prevent wrapping
    content = content.replace('<td class="py-3.5 px-4 text-center">', '<td class="py-3.5 px-4 text-center whitespace-nowrap">')
    
    # And we can also wrap the buttons inside a flex container.
    # But whitespace-nowrap alone forces inline elements to stay on the same line!
    # So `whitespace-nowrap` is enough.
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Fixed actions alignment in {f}')
