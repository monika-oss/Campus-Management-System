import glob
import re

def fix_scrollbar_hide():
    html_files = glob.glob('**/*.html', recursive=True)
    html_files = [f for f in html_files if 'backend' not in f and '.venv' not in f and 'node_modules' not in f]
    
    css_to_inject = """
        /* Hide all scrollbars visually but keep scroll functionality */
        ::-webkit-scrollbar { display: none; }
        * { scrollbar-width: none; -ms-overflow-style: none; }
"""
    
    modified_count = 0
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Only add if not already added
            if 'scrollbar-width: none' not in content:
                # Find the </style> tag and inject just before it, or inject before </head>
                if '</style>' in content:
                    # Inject before the last </style> tag
                    idx = content.rfind('</style>')
                    content = content[:idx] + css_to_inject + content[idx:]
                elif '</head>' in content:
                    # Inject a <style> block before </head>
                    idx = content.rfind('</head>')
                    style_block = f"\n    <style>{css_to_inject}    </style>\n"
                    content = content[:idx] + style_block + content[idx:]
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_count += 1
                print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            
    print(f"Finished updating {modified_count} files.")

if __name__ == '__main__':
    fix_scrollbar_hide()
