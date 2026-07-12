import os

dir_path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin'
nav_snippet = '''
                <div class="flex items-center gap-6">
                    <div class="relative cursor-pointer hover:text-blue-600 transition-colors flex items-center justify-center" id="bellNotify">
                        <i data-lucide="bell" class="w-6 h-6 text-slate-600"></i>
                        <span class="absolute -top-1.5 -right-1.5 bg-red-500 text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold">3</span>
                    </div>
                    <div class="flex items-center gap-3 border-l border-slate-150 pl-6">
                        <div class="w-9 h-9 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-sm shadow-sm" id="userAvatar">A</div>
                        <span class="font-semibold text-slate-700 text-sm" id="userName">Admin</span>
                    </div>
                </div>'''

for fname in ['results.html', 'leave.html', 'attendance.html', 'announcements.html']:
    path = os.path.join(dir_path, fname)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'bellNotify' not in content:
            content = content.replace('</header>', f'{nav_snippet}\n            </header>')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added navbar profile to {fname}")
