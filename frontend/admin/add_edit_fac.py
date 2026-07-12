import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

edit_modal_html = """
    <!-- Edit Faculty Modal -->
    <div class="modal-overlay hidden fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center" id="editFacultyModal">
        <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full m-4 overflow-hidden border border-slate-100 transform scale-95" id="editFacultyModalContent">
            <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                <h3 class="text-lg font-bold text-slate-800 font-outfit">Edit Faculty</h3>
                <button class="text-slate-400 hover:text-slate-650 text-xl font-bold focus:outline-none" onclick="utils.hideModal('editFacultyModal')">×</button>
            </div>
            <div class="p-6">
                <form id="editFacultyForm" class="space-y-4">
                    <input type="hidden" id="ef_id">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Name*</label>
                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="ef_name" required>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Email Address*</label>
                        <input type="email" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="ef_email" required>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Department*</label>
                        <select class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="ef_dept" required>
                            <option value="">Select Department</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Designation</label>
                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="ef_desig">
                    </div>
                </form>
            </div>
            <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
                <button class="px-4 py-2 border border-slate-300 text-slate-600 rounded-lg hover:bg-slate-100 font-medium text-sm transition-colors" onclick="utils.hideModal('editFacultyModal')">Cancel</button>
                <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-sm transition-colors shadow-sm" id="updateFacultyBtn">Update</button>
            </div>
        </div>
    </div>
"""
content = content.replace('<!-- Scripts -->', edit_modal_html + '\n    <!-- Scripts -->')

search_row = '<button class="p-1 px-3 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg text-xs font-semibold transition-colors" onclick="deleteFaculty(${f.faculty_id})">🗑️ Delete</button>'
replace_row = '<button class="p-1 px-3 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-600 hover:text-white rounded-lg text-xs font-semibold transition-colors mr-2" onclick="openEditFacultyModal(${f.faculty_id})">✏️ Edit</button>\n                                ' + search_row
content = content.replace(search_row, replace_row)

search_dept = "const opt = document.createElement('option');\n                    opt.value = d.id;\n                    opt.textContent = `${d.code} - ${d.name}`;\n                    fDept.appendChild(opt);"
replace_dept = search_dept + "\n\n                    const optEdit = document.createElement('option');\n                    optEdit.value = d.id;\n                    optEdit.textContent = `${d.code} - ${d.name}`;\n                    document.getElementById('ef_dept').appendChild(optEdit);"
content = content.replace(search_dept, replace_dept)

edit_js = """
        window.openEditFacultyModal = async function(id) {
            try {
                const f = await api.get('/faculty/' + id + '/');
                document.getElementById('ef_id').value = f.faculty_id;
                document.getElementById('ef_name').value = f.name;
                document.getElementById('ef_email').value = f.email;
                document.getElementById('ef_dept').value = f.department;
                document.getElementById('ef_desig').value = f.designation || '';
                utils.showModal('editFacultyModal');
            } catch(e) {
                utils.showToast('Error loading faculty details', 'error');
            }
        };

        document.getElementById('updateFacultyBtn').addEventListener('click', async () => {
            const form = document.getElementById('editFacultyForm');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            const id = document.getElementById('ef_id').value;
            const data = {
                name: document.getElementById('ef_name').value,
                email: document.getElementById('ef_email').value,
                department: document.getElementById('ef_dept').value,
                designation: document.getElementById('ef_desig').value,
            };
            try {
                await api.put('/faculty/' + id + '/', data);
                utils.showToast('Faculty updated successfully', 'success');
                utils.hideModal('editFacultyModal');
                loadFaculty();
            } catch (e) {
                utils.showToast('Error updating faculty', 'error');
            }
        });
"""
content = content.replace('async function deleteFaculty(id)', edit_js + '\n        async function deleteFaculty(id)')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated faculty.html')
