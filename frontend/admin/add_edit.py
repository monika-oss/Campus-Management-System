import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\students.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

edit_modal_html = """
    <!-- Edit Student Modal -->
    <div class="modal-overlay hidden fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center" id="editStudentModal">
        <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full m-4 overflow-hidden border border-slate-100 transform scale-95" id="editStudentModalContent">
            <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                <h3 class="text-lg font-bold text-slate-800 font-outfit">Edit Student</h3>
                <button class="text-slate-400 hover:text-slate-650 text-xl font-bold focus:outline-none" onclick="utils.hideModal('editStudentModal')">×</button>
            </div>
            <div class="p-6">
                <form id="editStudentForm" class="space-y-4">
                    <input type="hidden" id="e_id">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Name*</label>
                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="e_name" required>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Register Number*</label>
                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="e_reg" required>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Email Address*</label>
                        <input type="email" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="e_email" required>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Department*</label>
                        <select class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="e_dept" required>
                            <option value="">Select Department</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Year (1-4)*</label>
                        <input type="number" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="e_year" min="1" max="4" required>
                    </div>
                </form>
            </div>
            <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
                <button class="px-4 py-2 border border-slate-300 text-slate-600 rounded-lg hover:bg-slate-100 font-medium text-sm transition-colors" onclick="utils.hideModal('editStudentModal')">Cancel</button>
                <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-sm transition-colors shadow-sm" id="updateStudentBtn">Update</button>
            </div>
        </div>
    </div>
"""
content = content.replace('<!-- Scripts -->', edit_modal_html + '\n    <!-- Scripts -->')

search_row = '<button class="p-1 px-3 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg text-xs font-semibold transition-colors" onclick="deleteStudent(${s.student_id})">🗑️ Delete</button>'
replace_row = '<button class="p-1 px-3 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-600 hover:text-white rounded-lg text-xs font-semibold transition-colors mr-2" onclick="openEditStudentModal(${s.student_id})">✏️ Edit</button>\n                                ' + search_row
content = content.replace(search_row, replace_row)

search_dept = "const optForm = document.createElement('option');\n                        optForm.value = d.id;\n                        optForm.textContent = `${d.code} - ${d.name}`;\n                        sDept.appendChild(optForm);"
replace_dept = search_dept + "\n\n                        const optEdit = document.createElement('option');\n                        optEdit.value = d.id;\n                        optEdit.textContent = `${d.code} - ${d.name}`;\n                        document.getElementById('e_dept').appendChild(optEdit);"
content = content.replace(search_dept, replace_dept)

edit_js = """
        window.openEditStudentModal = async function(id) {
            try {
                const s = await api.get('/students/' + id + '/');
                document.getElementById('e_id').value = s.student_id;
                document.getElementById('e_name').value = s.name;
                document.getElementById('e_reg').value = s.roll_number;
                document.getElementById('e_email').value = s.email;
                document.getElementById('e_dept').value = s.department;
                document.getElementById('e_year').value = s.year;
                utils.showModal('editStudentModal');
            } catch(e) {
                utils.showToast('Error loading student details', 'error');
            }
        };

        document.getElementById('updateStudentBtn').addEventListener('click', async () => {
            const form = document.getElementById('editStudentForm');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            const id = document.getElementById('e_id').value;
            const data = {
                name: document.getElementById('e_name').value,
                roll_number: document.getElementById('e_reg').value,
                email: document.getElementById('e_email').value,
                department: document.getElementById('e_dept').value,
                year: document.getElementById('e_year').value,
            };
            try {
                await api.put('/students/' + id + '/', data);
                utils.showToast('Student updated successfully', 'success');
                utils.hideModal('editStudentModal');
                loadStudents();
            } catch (e) {
                utils.showToast('Error updating student', 'error');
            }
        });
"""
content = content.replace('async function deleteStudent(id)', edit_js + '\n        async function deleteStudent(id)')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated students.html')
