import os
import glob
import re

def fix_h_screen():
    html_files = glob.glob('**/*.html', recursive=True)
    html_files = [f for f in html_files if 'backend' not in f and '.venv' not in f and 'node_modules' not in f]
    
    modified_count = 0
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace all occurrences of h-screen with h-[100dvh] globally
            # But make sure we only match the whole word h-screen
            content = re.sub(r'\bh-screen\b', 'h-[100dvh]', content)
            
            # Also, change min-h-screen to min-h-[100dvh] just in case
            content = re.sub(r'\bmin-h-screen\b', 'min-h-[100dvh]', content)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_count += 1
                print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            
    print(f"Finished updating {modified_count} files.")

if __name__ == '__main__':
    fix_h_screen()
