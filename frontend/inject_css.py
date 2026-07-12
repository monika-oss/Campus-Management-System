import os
import glob

css_link = '    <link rel="stylesheet" href="../css/premium-theme.css?v=6">\n'

def inject_css(directory):
    for filepath in glob.glob(os.path.join(directory, '*.html')):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'premium-theme.css' not in content:
            if '</head>' in content:
                content = content.replace('</head>', f'{css_link}</head>')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'Updated {filepath}')
            else:
                print(f'No </head> in {filepath}')
        else:
            print(f'Already has premium-theme.css: {filepath}')

inject_css('admin')
inject_css('faculty')
inject_css('student')
