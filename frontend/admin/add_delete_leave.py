import re

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\leave.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the inner HTML of the actions cell
old_actions = '''${l.status === 'pending' ? `
                                    <div class="flex items-center justify-center gap-1.5">
                                        <button class="p-1.5 px-2 bg-emerald-50 text-emerald-600 border border-emerald-200 hover:bg-emerald-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="updateLeave(${l.leave_id}, 'approve')" title="Approve"><i class="bi bi-check-circle"></i></button>
                                        <button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm ml-2" onclick="updateLeave(${l.leave_id}, 'reject')" title="Reject"><i class="bi bi-x-circle"></i></button>
                                    </div>
                                ` : '<span class="text-slate-400 font-medium">-</span>'}'''

new_actions = '''<div class="flex items-center justify-center gap-1.5">
                                    ${l.status === 'pending' ? `
                                        <button class="p-1.5 px-2 bg-emerald-50 text-emerald-600 border border-emerald-200 hover:bg-emerald-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="updateLeave(${l.leave_id}, 'approve')" title="Approve"><i class="bi bi-check-circle"></i></button>
                                        <button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="updateLeave(${l.leave_id}, 'reject')" title="Reject"><i class="bi bi-x-circle"></i></button>
                                    ` : ''}
                                    <button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="deleteLeave(${l.leave_id})" title="Delete"><i class="bi bi-trash"></i></button>
                                </div>'''

content = content.replace(old_actions, new_actions)

js_logic = '''
        window.deleteLeave = async function(id) {
            if(confirm('Are you sure you want to delete this leave request?')) {
                try {
                    await api.delete('/leave/' + id + '/');
                    utils.showToast('Deleted successfully', 'success');
                    loadLeaves();
                } catch(e) {
                    utils.showToast('Error deleting', 'error');
                }
            }
        };
'''
if 'window.deleteLeave' not in content:
    content = content.replace('async function loadLeaves()', js_logic + '\n        async function loadLeaves()')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated leave.html')
