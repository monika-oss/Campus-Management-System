import os
import glob
import re

def fix_sidebar_scroll():
    html_files = glob.glob('**/*.html', recursive=True)
    html_files = [f for f in html_files if 'backend' not in f and '.venv' not in f and 'node_modules' not in f]
    
    modified_count = 0
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. Replace h-screen with h-[100dvh] on aside
            content = re.sub(r'(<aside[^>]*\b)h-screen(\b[^>]*>)', r'\1h-[100dvh]\2', content)
            
            # 2. Add flex-1 overflow-y-auto to the div containing the logo and nav
            # The structure is:
            # <aside ... id="adminSidebar">
            #     <div>
            #         <!-- Brand logo -->
            
            def replace_first_div(match):
                # match.group(1) is the <aside ...> tag
                aside_tag = match.group(1)
                inner = match.group(2)
                # find the first <div> and replace with <div class="flex-1 overflow-y-auto">
                inner = re.sub(r'<div>', r'<div class="flex-1 overflow-y-auto">', inner, count=1)
                return aside_tag + inner
            
            content = re.sub(r'(<aside[^>]*id="[a-zA-Z]*Sidebar"[^>]*>)\s*(<div>)', replace_first_div, content)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_count += 1
                print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            
    print(f"Finished updating {modified_count} files.")

if __name__ == '__main__':
    fix_sidebar_scroll()
