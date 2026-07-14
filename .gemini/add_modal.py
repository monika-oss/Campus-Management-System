import os

admin_faculty = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\admin\faculty.html'

with open(admin_faculty, 'r', encoding='utf-8') as f:
    html = f.read()

modal_html = """
    <!-- Add Dept Modal -->
    <div class="modal-overlay hidden fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center" id="addDeptModal">
        <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full m-4 overflow-hidden border border-slate-100 transform scale-95" id="addDeptModalContent">
            <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                <h3 class="text-lg font-bold text-slate-800 font-outfit">Add New Department</h3>
                <button class="text-slate-400 hover:text-slate-650 text-xl font-bold focus:outline-none" onclick="utils.hideModal('addDeptModal')">×</button>
            </div>
            <div class="p-6">
                <form id="deptForm" class="space-y-4">
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Department Code*</label>
                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="d_code" placeholder="e.g. CSE" required>
                    </div>
                    <div>
                        <label class="block text-slate-700 font-semibold mb-1 text-sm">Department Name*</label>
                        <input type="text" class="ant-input w-full border border-slate-300 focus:border-blue-500 focus:outline-none" id="d_name" placeholder="e.g. Computer Science" required>
                    </div>
                </form>
            </div>
            <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
                <button class="px-4 py-2 border border-slate-300 text-slate-600 rounded-lg hover:bg-slate-100 font-medium text-sm transition-colors" onclick="utils.hideModal('addDeptModal')">Cancel</button>
                <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-sm transition-colors shadow-sm" id="saveDeptBtn">Save</button>
            </div>
        </div>
    </div>
"""

js_logic = """
            document.getElementById('saveDeptBtn').addEventListener('click', async (e) => {
                const form = document.getElementById('deptForm');
                if (!form.checkValidity()) {
                    form.reportValidity();
                    return;
                }
                
                const data = {
                    code: document.getElementById('d_code').value.toUpperCase(),
                    name: document.getElementById('d_name').value
                };

                try {
                    await api.post('/students/departments/', data);
                    utils.showToast('Department added successfully', 'success');
                    utils.hideModal('addDeptModal');
                    document.getElementById('deptForm').reset();
                    window.location.reload();
                } catch (e) {
                    utils.showToast('Error adding department (Code might already exist)', 'error');
                }
            });
"""

# Insert modal HTML
if 'id="addDeptModal"' not in html:
    html = html.replace('<!-- Add Faculty Modal -->', modal_html + '\n    <!-- Add Faculty Modal -->')

# Insert JS logic
if "document.getElementById('saveDeptBtn')" not in html:
    html = html.replace("document.getElementById('saveFacultyBtn').addEventListener", js_logic + "\n            document.getElementById('saveFacultyBtn').addEventListener")

with open(admin_faculty, 'w', encoding='utf-8') as f:
    f.write(html)

print("Modal added successfully.")
