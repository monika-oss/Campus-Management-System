import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\attendance.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Bootstrap Icons if not present
if 'bootstrap-icons.min.css' not in content:
    content = content.replace('</head>', '    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">\n</head>')

# 2. Add Actions column header
header_search = '<th class="py-3 px-4">Status</th>'
header_replace = '<th class="py-3 px-4">Status</th>\n                                    <th class="py-3 px-4 text-center">Actions</th>'
if header_search in content:
    content = content.replace(header_search, header_replace)

# 3. Add Edit/Delete buttons in JS template
js_search = 'border-amber-200\'}">${a.status}</span>\\n                            </td>\\n                        </tr>'
js_replace = '''border-amber-200\'}">${a.status}</span>
                            </td>
                            <td class="py-3.5 px-4 text-center">
                                <button class="p-1.5 px-2 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-600 hover:text-white rounded-lg transition-colors mr-2 shadow-sm" onclick="openEditAttendanceModal(${a.attendance_id})" title="Edit"><i class="bi bi-pencil-square"></i></button>
                                <button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="deleteAttendance(${a.attendance_id})" title="Delete"><i class="bi bi-trash"></i></button>
                            </td>
                        </tr>'''
if js_search in content:
    content = content.replace(js_search, js_replace)

# 4. Add Edit Modal
edit_modal = '''
    <!-- Edit Attendance Modal -->
    <div class="modal-overlay hidden fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center" id="editAttendanceModal">
        <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full m-4 overflow-hidden border border-slate-100 transform scale-95" id="editAttendanceModalContent">
            <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                <h3 class="text-lg font-bold text-slate-800 font-outfit">Edit Attendance</h3>
                <button class="text-slate-400 hover:text-slate-600 text-xl font-bold focus:outline-none" onclick="utils.hideModal('editAttendanceModal')">×</button>
            </div>
            <div class="p-6">
                <form id="editAttendanceForm" class="space-y-4">
                    <input type="hidden" id="ea_id">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Status</label>
                        <select class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="ea_status" required>
                            <option value="present">Present</option>
                            <option value="absent">Absent</option>
                            <option value="late">Late</option>
                            <option value="excused">Excused</option>
                        </select>
                    </div>
                </form>
            </div>
            <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
                <button class="px-4 py-2 border border-slate-300 text-slate-600 rounded-lg hover:bg-slate-100 font-medium text-sm transition-colors" onclick="utils.hideModal('editAttendanceModal')">Cancel</button>
                <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-sm transition-colors shadow-sm" id="updateAttendanceBtn">Update</button>
            </div>
        </div>
    </div>
'''
if 'editAttendanceModal' not in content:
    content = content.replace('<!-- Scripts -->', edit_modal + '\n    <!-- Scripts -->')

# 5. Add Edit/Delete JS logic
js_logic = '''
        window.openEditAttendanceModal = async function(id) {
            try {
                const a = await api.get('/attendance/' + id + '/');
                document.getElementById('ea_id').value = a.attendance_id;
                document.getElementById('ea_status').value = a.status;
                utils.showModal('editAttendanceModal');
            } catch(e) {
                utils.showToast('Error loading details', 'error');
            }
        };

        document.getElementById('updateAttendanceBtn').addEventListener('click', async () => {
            const form = document.getElementById('editAttendanceForm');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            const id = document.getElementById('ea_id').value;
            try {
                const existing = await api.get('/attendance/' + id + '/');
                const data = {
                    student: existing.student,
                    subject: existing.subject,
                    date: existing.date,
                    status: document.getElementById('ea_status').value
                };
                await api.put('/attendance/' + id + '/', data);
                utils.showToast('Updated successfully', 'success');
                utils.hideModal('editAttendanceModal');
                loadAttendance();
            } catch (e) {
                utils.showToast('Error updating', 'error');
            }
        });

        window.deleteAttendance = async function(id) {
            if(confirm('Are you sure you want to delete this record?')) {
                try {
                    await api.delete('/attendance/' + id + '/');
                    utils.showToast('Deleted successfully', 'success');
                    loadAttendance();
                } catch(e) {
                    utils.showToast('Error deleting', 'error');
                }
            }
        };
'''
if 'window.deleteAttendance' not in content:
    # Need to find loadAttendance function, wait there is no loadAttendance, it's inside DOMContentLoaded inline.
    pass

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated attendance.html partially')
