import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\announcements.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Bootstrap Icons if not present
if 'bootstrap-icons.min.css' not in content:
    content = content.replace('</head>', '    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">\n</head>')

# 2. Add Actions column header
header_search = '<th class="py-3 px-4">Status</th>'
header_replace = '<th class="py-3 px-4">Status</th>\n                                    <th class="py-3 px-4 text-center">Actions</th>'
content = content.replace(header_search, header_replace)

# 3. Add Edit/Delete buttons in JS template
js_search = 'Inactive\'}</span></td>\\n                            </tr>'
js_replace = '''Inactive'}</span></td>
                                <td class="py-3.5 px-4 text-center">
                                    <button class="p-1.5 px-2 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-600 hover:text-white rounded-lg transition-colors mr-2 shadow-sm" onclick="openEditNotificationModal(${n.notification_id})" title="Edit"><i class="bi bi-pencil-square"></i></button>
                                    <button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="deleteNotification(${n.notification_id})" title="Delete"><i class="bi bi-trash"></i></button>
                                </td>
                            </tr>'''
content = content.replace(js_search, js_replace)

# 4. Add Edit Modal
edit_modal = '''
    <!-- Edit Notification Modal -->
    <div class="modal-overlay hidden fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center" id="editNotificationModal">
        <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full m-4 overflow-hidden border border-slate-100 transform scale-95" id="editNotificationModalContent">
            <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                <h3 class="text-lg font-bold text-slate-800 font-outfit">Edit Announcement</h3>
                <button class="text-slate-400 hover:text-slate-600 text-xl font-bold focus:outline-none" onclick="utils.hideModal('editNotificationModal')">×</button>
            </div>
            <div class="p-6">
                <form id="editNotificationForm" class="space-y-4">
                    <input type="hidden" id="en_id">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Title*</label>
                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="en_title" required>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Description*</label>
                        <textarea class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none min-h-[100px]" id="en_desc" required></textarea>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Target Audience*</label>
                        <select class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="en_target" required>
                            <option value="all">Everyone</option>
                            <option value="student">Students Only</option>
                            <option value="faculty">Faculty Only</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Status</label>
                        <select class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="en_status" required>
                            <option value="true">Active</option>
                            <option value="false">Inactive</option>
                        </select>
                    </div>
                </form>
            </div>
            <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
                <button class="px-4 py-2 border border-slate-300 text-slate-600 rounded-lg hover:bg-slate-100 font-medium text-sm transition-colors" onclick="utils.hideModal('editNotificationModal')">Cancel</button>
                <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-sm transition-colors shadow-sm" id="updateNotificationBtn">Update</button>
            </div>
        </div>
    </div>
'''
content = content.replace('<!-- Scripts -->', edit_modal + '\n    <!-- Scripts -->')

# 5. Add Edit/Delete JS logic
js_logic = '''
        window.openEditNotificationModal = async function(id) {
            try {
                const n = await api.get('/notifications/' + id + '/');
                document.getElementById('en_id').value = n.notification_id;
                document.getElementById('en_title').value = n.title;
                document.getElementById('en_desc').value = n.description;
                document.getElementById('en_target').value = n.target_role;
                document.getElementById('en_status').value = n.is_active ? 'true' : 'false';
                utils.showModal('editNotificationModal');
            } catch(e) {
                utils.showToast('Error loading details', 'error');
            }
        };

        document.getElementById('updateNotificationBtn').addEventListener('click', async () => {
            const form = document.getElementById('editNotificationForm');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            const id = document.getElementById('en_id').value;
            const data = {
                title: document.getElementById('en_title').value,
                description: document.getElementById('en_desc').value,
                target_role: document.getElementById('en_target').value,
                is_active: document.getElementById('en_status').value === 'true'
            };
            try {
                await api.put('/notifications/' + id + '/', data);
                utils.showToast('Updated successfully', 'success');
                utils.hideModal('editNotificationModal');
                loadNotifications();
            } catch (e) {
                utils.showToast('Error updating', 'error');
            }
        });

        window.deleteNotification = async function(id) {
            if(confirm('Are you sure you want to delete this announcement?')) {
                try {
                    await api.delete('/notifications/' + id + '/');
                    utils.showToast('Deleted successfully', 'success');
                    loadNotifications();
                } catch(e) {
                    utils.showToast('Error deleting', 'error');
                }
            }
        };
'''
content = content.replace('async function loadNotifications()', js_logic + '\n        async function loadNotifications()')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated announcements.html')
