import glob
import re

def fix_pagination_and_overflow():
    html_files = glob.glob('**/*.html', recursive=True)
    html_files = [f for f in html_files if 'backend' not in f and '.venv' not in f and 'node_modules' not in f]
    
    modified_count = 0
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content

            # 1. Reduce ITEMS_PER_PAGE from 6 to 5 to prevent y-scroll on mobile
            content = re.sub(r'const ITEMS_PER_PAGE = \d+;', 'const ITEMS_PER_PAGE = 5;', content)

            # 2. On the table wrapper div, change overflow-y-hidden to [clip-path style]: 
            # use style="overflow-y: clip" on the table wrapper to properly clip
            # Replace: class="overflow-x-auto overflow-y-hidden"
            # With:    class="overflow-x-auto" style="overflow-y: clip"
            content = re.sub(
                r'class="overflow-x-auto overflow-y-hidden"',
                'class="overflow-x-auto" style="overflow-y: clip"',
                content
            )

            # 3. Also replace plain overflow-x-auto on table wrappers that wrap a table
            # We already handled overflow-y-hidden above, but let's also handle plain overflow-x-auto
            # where the table is wrapped

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_count += 1
                print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            
    print(f"Finished updating {modified_count} files.")

if __name__ == '__main__':
    fix_pagination_and_overflow()
