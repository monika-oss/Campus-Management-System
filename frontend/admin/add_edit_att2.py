import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\attendance.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Refine JS insert
js_logic = '''
        async function loadAttendanceData() {
            try {
                const data = await api.get('/attendance/');
                const tbody = document.querySelector('#attendanceTable tbody');
                
                if (data.length) {
                    tbody.innerHTML = data.map(a => `
                        <tr>
                            <td class="py-3.5 px-4 font-semibold text-slate-800">${a.date}</td>
                            <td class="py-3.5 px-4 font-medium">${a.student_details?.name} <span class="text-xs text-slate-400 font-normal">(${a.student_details?.roll_number})</span></td>
                            <td class="py-3.5 px-4">${a.subject_details?.subject_name || 'General Class'}</td>
                            <td class="py-3.5 px-4">
                                <span class="px-2.5 py-1 text-xs font-semibold rounded-full ${a.status === 'present' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : a.status === 'absent' ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-amber-50 text-amber-700 border border-amber-200'}">${a.status}</span>
                            </td>
                            <td class="py-3.5 px-4 text-center">
                                <button class="p-1.5 px-2 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-600 hover:text-white rounded-lg transition-colors mr-2 shadow-sm" onclick="openEditAttendanceModal(${a.attendance_id})" title="Edit"><i class="bi bi-pencil-square"></i></button>
                                <button class="p-1.5 px-2 bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-600 hover:text-white rounded-lg transition-colors shadow-sm" onclick="deleteAttendance(${a.attendance_id})" title="Delete"><i class="bi bi-trash"></i></button>
                            </td>
                        </tr>
                    `).join('');
                } else {
                    tbody.innerHTML = '<tr><td colspan="5" class="py-8 text-center text-slate-400">No attendance records found.</td></tr>';
                }
            } catch (e) {
                console.error(e);
            }
        }

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

        document.getElementById('updateAttendanceBtn')?.addEventListener('click', async () => {
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
                loadAttendanceData();
            } catch (e) {
                utils.showToast('Error updating', 'error');
            }
        });

        window.deleteAttendance = async function(id) {
            if(confirm('Are you sure you want to delete this record?')) {
                try {
                    await api.delete('/attendance/' + id + '/');
                    utils.showToast('Deleted successfully', 'success');
                    loadAttendanceData();
                } catch(e) {
                    utils.showToast('Error deleting', 'error');
                }
            }
        };
'''

# Replace the inner try-catch with a call to loadAttendanceData
import re
content = re.sub(
    r'try \{\s+const data = await api\.get\(\'/attendance/\'\);.*?console\.error\(e\);\s+\}',
    'await loadAttendanceData();',
    content,
    flags=re.DOTALL
)

if 'async function loadAttendanceData()' not in content:
    content = content.replace('</script>\n    <script src="../js/animations.js">', js_logic + '\n    </script>\n    <script src="../js/animations.js">')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated attendance.html fully')
