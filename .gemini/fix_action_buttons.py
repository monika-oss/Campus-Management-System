import os
import glob
import re

def fix_action_buttons_mobile():
    html_files = glob.glob('**/*.html', recursive=True)
    html_files = [f for f in html_files if 'backend' not in f and '.venv' not in f and 'node_modules' not in f]
    
    modified_count = 0
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Find the action buttons container:
            # <div class="flex flex-row items-center gap-2 w-full md:w-auto justify-start md:justify-end">
            # We want to add flex-wrap so the buttons wrap on mobile instead of squishing and hiding icons
            content = re.sub(
                r'class="flex flex-row items-center gap-2 w-full md:w-auto justify-start md:justify-end"',
                r'class="flex flex-row flex-wrap items-center gap-2 w-full md:w-auto justify-start md:justify-end"',
                content
            )
            
            # Also ensure all buttons inside this container have shrink-0 if they don't already
            # Actually, flex-wrap on the container is enough to prevent flex items from shrinking below their content size
            # But let's also add shrink-0 to the icons just in case:
            # <i data-lucide="..." class="...">
            # This is harder to do safely with regex globally, but we can do it for typical w-4 h-4
            content = re.sub(
                r'(<i\s+data-lucide="[^"]*"\s+class="[^"]*\bw-4 h-4\b)([^"]*">)',
                lambda m: (m.group(1) + ' shrink-0' + m.group(2)) if 'shrink-0' not in m.group(0) else m.group(0),
                content
            )
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_count += 1
                print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            
    print(f"Finished updating {modified_count} files.")

if __name__ == '__main__':
    fix_action_buttons_mobile()
