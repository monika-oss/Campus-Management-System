import os

auth_js_path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\js\auth.js'
with open(auth_js_path, 'r', encoding='utf-8') as f:
    auth_content = f.read()

profile_js = '''
// Auto-update profile name in navbar
document.addEventListener('DOMContentLoaded', () => {
    const user = auth.getUser();
    if (user && document.getElementById('userName')) {
        const name = user.name || (user.email ? user.email.split('@')[0] : 'Admin');
        document.getElementById('userName').innerText = name;
        document.getElementById('userAvatar').innerText = name.charAt(0).toUpperCase();
    }
});
'''
if 'Auto-update profile name in navbar' not in auth_content:
    with open(auth_js_path, 'a', encoding='utf-8') as f:
        f.write('\n' + profile_js)


# Update HTML files
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

for fname in os.listdir(dir_path):
    if fname.endswith('.html') and fname != 'dashboard.html':
        path = os.path.join(dir_path, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '<header ' in content and 'id="topNavbar"' in content and 'bellNotify' not in content:
            # Inject before </header>
            content = content.replace('</header>', f'{nav_snippet}\n            </header>')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added navbar profile to {fname}")

