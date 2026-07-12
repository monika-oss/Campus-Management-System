import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\results.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Bootstrap Icons if not present
if 'bootstrap-icons.min.css' not in content:
    content = content.replace('</head>', '    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">\n</head>')

# 2. Add Actions column header
header_search = '<th class="py-3 px-4">Published</th>'
header_replace = '<th class="py-3 px-4">Published</th>\n                                    <th class="py-3 px-4 text-center">Actions</th>'
if header_search in content:
    content = content.replace(header_search, header_replace)

# 3. Add Edit/Delete buttons in JS template
js_search = 'border-amber-200\'}">${r.is_published ? \'Yes\' : \'No\'}</span>\\n                            </td>\\n                        </tr>'
js_replace = '''border-amber-200\'}">${r.is_published ? 'Yes' : 'No'}</span>
                            </td>
                            <td class="py-3.5 px-4 text-center">
                                <button class="p-1.5 px-2 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-600 hover:text-white rounded-lg transition-colors mr-2 shadow-sm" onclick="openEditResultModal(${r.result_id})" title="Edit"><i class="bi bi-pencil-square"></i></button>
                                <button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="deleteResult(${r.result_id})" title="Delete"><i class="bi bi-trash"></i></button>
                            </td>
                        </tr>'''
if js_search in content:
    content = content.replace(js_search, js_replace)

# 4. Add Edit Modal
edit_modal = '''
    <!-- Edit Result Modal -->
    <div class="modal-overlay hidden fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center" id="editResultModal">
        <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full m-4 overflow-hidden border border-slate-100 transform scale-95" id="editResultModalContent">
            <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                <h3 class="text-lg font-bold text-slate-800 font-outfit">Edit Result</h3>
                <button class="text-slate-400 hover:text-slate-600 text-xl font-bold focus:outline-none" onclick="utils.hideModal('editResultModal')">×</button>
            </div>
            <div class="p-6">
                <form id="editResultForm" class="space-y-4">
                    <input type="hidden" id="er_id">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Marks Obtained*</label>
                        <input type="number" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="er_marks" required>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Max Marks*</label>
                        <input type="number" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="er_max" required>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Published</label>
                        <select class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="er_published" required>
                            <option value="true">Yes</option>
                            <option value="false">No</option>
                        </select>
                    </div>
                </form>
            </div>
            <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
                <button class="px-4 py-2 border border-slate-300 text-slate-600 rounded-lg hover:bg-slate-100 font-medium text-sm transition-colors" onclick="utils.hideModal('editResultModal')">Cancel</button>
                <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-sm transition-colors shadow-sm" id="updateResultBtn">Update</button>
            </div>
        </div>
    </div>
'''
if 'editResultModal' not in content:
    content = content.replace('<!-- Scripts -->', edit_modal + '\n    <!-- Scripts -->')

# 5. Add Edit/Delete JS logic
js_logic = '''
        window.openEditResultModal = async function(id) {
            try {
                const r = await api.get('/results/' + id + '/');
                document.getElementById('er_id').value = r.result_id;
                document.getElementById('er_marks').value = r.marks_obtained;
                document.getElementById('er_max').value = r.max_marks;
                document.getElementById('er_published').value = r.is_published ? 'true' : 'false';
                utils.showModal('editResultModal');
            } catch(e) {
                utils.showToast('Error loading details', 'error');
            }
        };

        document.getElementById('updateResultBtn').addEventListener('click', async () => {
            const form = document.getElementById('editResultForm');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            const id = document.getElementById('er_id').value;
            // First fetch the existing result to preserve student, subject, year, semester
            try {
                const existing = await api.get('/results/' + id + '/');
                const data = {
                    student: existing.student,
                    subject: existing.subject,
                    year: existing.year,
                    semester: existing.semester,
                    marks_obtained: document.getElementById('er_marks').value,
                    max_marks: document.getElementById('er_max').value,
                    is_published: document.getElementById('er_published').value === 'true'
                };
                await api.put('/results/' + id + '/', data);
                utils.showToast('Updated successfully', 'success');
                utils.hideModal('editResultModal');
                loadResults();
            } catch (e) {
                utils.showToast('Error updating', 'error');
            }
        });

        window.deleteResult = async function(id) {
            if(confirm('Are you sure you want to delete this result?')) {
                try {
                    await api.delete('/results/' + id + '/');
                    utils.showToast('Deleted successfully', 'success');
                    loadResults();
                } catch(e) {
                    utils.showToast('Error deleting', 'error');
                }
            }
        };
'''
if 'window.deleteResult' not in content:
    content = content.replace('async function loadResults()', js_logic + '\n        async function loadResults()')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated results.html')
