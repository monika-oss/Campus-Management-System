import os
import glob
import re

def fix_html_files():
    # Find all html files except in venv, node_modules, backend
    html_files = glob.glob('**/*.html', recursive=True)
    html_files = [f for f in html_files if 'backend' not in f and '.venv' not in f and 'node_modules' not in f]
    
    modified_count = 0
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Update Overlay z-index
        # Look for class containing "fixed inset-0" and "z-40" or "z-50" or "z-[90]" and replace with "z-[90]"
        # Specifically targeting the overlay divs: id="adminSidebarOverlay", id="facultySidebarOverlay", etc.
        content = re.sub(r'(id="[^"]*SidebarOverlay"[^>]*class="[^"]*)(z-40|z-50)', r'\1z-[90]', content)
        
        # Also catch cases where id is before or after class
        # Let's just do a generic replace on the overlay div
        def replace_overlay(match):
            m = match.group(0)
            m = re.sub(r'z-40|z-50', 'z-[90]', m)
            return m
        content = re.sub(r'<div[^>]*id="[a-zA-Z]*SidebarOverlay"[^>]*>', replace_overlay, content)

        # 2. Update Sidebar z-index to z-[100]
        def replace_aside(match):
            m = match.group(0)
            # Replace z-50 with z-[100]
            m = re.sub(r'\bz-50\b', 'z-[100]', m)
            # Ensure fixed inset-y-0 left-0
            if 'fixed' not in m:
                m = m.replace('class="', 'class="fixed inset-y-0 left-0 ')
            else:
                if 'inset-y-0' not in m:
                    m = m.replace('fixed', 'fixed inset-y-0 left-0')
            return m
        content = re.sub(r'<aside[^>]*id="[a-zA-Z]*Sidebar"[^>]*>', replace_aside, content)
        
        # 3. Update Header z-index to z-30
        def replace_header(match):
            m = match.group(0)
            m = re.sub(r'\bz-50\b', 'z-30', m)
            return m
        content = re.sub(r'<header[^>]*id="topNavbar"[^>]*>', replace_header, content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
            modified_count += 1
            
    print(f"Finished updating {modified_count} files.")

if __name__ == '__main__':
    fix_html_files()
