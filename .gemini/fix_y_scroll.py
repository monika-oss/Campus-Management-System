import glob
import re

def fix_y_scroll():
    html_files = glob.glob('**/*.html', recursive=True)
    html_files = [f for f in html_files if 'backend' not in f and '.venv' not in f and 'node_modules' not in f]
    
    modified_count = 0
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace all occurrences of class="overflow-x-auto" with class="overflow-x-auto overflow-y-hidden"
            # Some might have other classes like "overflow-x-auto p-4 lg:p-6"
            content = re.sub(r'class="([^"]*\boverflow-x-auto\b[^"]*)"', lambda m: 'class="' + m.group(1) + ' overflow-y-hidden"' if 'overflow-y-hidden' not in m.group(1) else m.group(0), content)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_count += 1
                print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            
    print(f"Finished updating {modified_count} files.")

if __name__ == '__main__':
    fix_y_scroll()
