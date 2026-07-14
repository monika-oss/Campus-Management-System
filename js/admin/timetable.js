// Admin Timetable Logic
document.addEventListener('DOMContentLoaded', async () => {
    lucide.createIcons();
    if (!auth.checkAuth() || !auth.hasRole('admin')) return;


    loadDepartments();
    loadSubjects();
    loadFaculty();
    loadTimetable();

    // Event listener for form
    const form = document.getElementById('addTimetableForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                department: document.getElementById('ttDept').value,
                year: document.getElementById('ttYear').value,
                section: '', // Setting blank section
                day_of_week: document.getElementById('ttDay').value,
                period_number: document.getElementById('ttPeriod').value,
                start_time: document.getElementById('ttStartTime').value,
                end_time: document.getElementById('ttEndTime').value,
                subject: document.getElementById('ttSubject').value,
                faculty: document.getElementById('ttFaculty').value
            };
            
            try {
                if (window.editingTimetableId) {
                    await api.put(`/students/timetable/${window.editingTimetableId}/`, payload);
                    utils.showToast('Timetable updated successfully', 'success');
                } else {
                    await api.post('/students/timetable/', payload);
                    utils.showToast('Timetable assigned successfully', 'success');
                }
                utils.hideModal('addTimetableModal');
                form.reset();
                window.editingTimetableId = null;
                loadTimetable();
            } catch (err) {
                console.error(err);
                utils.showToast('Error saving timetable', 'error');
            }
        });
    }

    // Reset editing ID when hiding modal manually if needed
    window.openAddModal = () => {
        window.editingTimetableId = null;
        if(form) {
            form.reset();
            document.querySelector('#addTimetableModalContent h3').innerText = 'Assign Timetable';
            document.querySelector('#addTimetableForm button[type="submit"]').innerText = 'Assign';
        }
        utils.showModal('addTimetableModal');
    };
});

async function loadDepartments() {
    try {
        const departments = await api.get('/students/departments/');
        const select = document.getElementById('ttDept');
        if (!select) return;
        select.innerHTML = '<option value="">Select Dept</option>';
        departments.forEach(d => {
            select.innerHTML += `<option value="${d.id}">${d.name} (${d.code})</option>`;
        });
    } catch (e) {
        console.error(e);
    }
}

async function loadSubjects() {
    try {
        const subjects = await api.get('/students/subjects/');
        const select = document.getElementById('ttSubject');
        if (!select) return;
        select.innerHTML = '<option value="">Select Subject</option>';
        subjects.forEach(s => {
            select.innerHTML += `<option value="${s.subject_id}">${s.subject_name}</option>`;
        });
    } catch (e) {
        console.error(e);
    }
}

async function loadFaculty() {
    try {
        const facultyList = await api.get('/faculty/');
        const select = document.getElementById('ttFaculty');
        if (!select) return;
        select.innerHTML = '<option value="">Select Faculty</option>';
        facultyList.forEach(f => {
            select.innerHTML += `<option value="${f.faculty_id}">${f.name}</option>`;
        });
    } catch (e) {
        console.error(e);
    }
}

async function loadTimetable() {
    try {
        const timetableList = await api.get('/students/timetable/');
        const tbody = document.getElementById('timetableTableBody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        if (timetableList.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-slate-500">No timetable entries found.</td></tr>`;
            return;
        }

        timetableList.forEach(tt => {
            tbody.innerHTML += `
                <tr class="hover:bg-slate-50/50 transition-colors">
                    <td class="py-4 px-6 text-slate-700 font-medium whitespace-nowrap">${tt.day_of_week}</td>
                    <td class="py-4 px-6 text-slate-600 whitespace-nowrap">Period ${tt.period_number}</td>
                    <td class="py-4 px-6 text-slate-600 whitespace-nowrap"><span class="bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-md text-xs font-semibold whitespace-nowrap">${tt.start_time ? tt.start_time.substring(0, 5) : '09:00'} - ${tt.end_time ? tt.end_time.substring(0, 5) : '09:50'}</span></td>
                    <td class="py-4 px-6 text-slate-600 whitespace-nowrap">Yr ${tt.year}</td>
                    <td class="py-4 px-6 text-slate-600 font-semibold whitespace-nowrap">${tt.department}</td>
                    <td class="py-4 px-6 text-slate-600">${tt.subject_details ? tt.subject_details.subject_name : 'Subject ' + tt.subject}</td>
                    <td class="py-4 px-6 text-slate-600">${tt.faculty_name || 'Faculty ' + tt.faculty}</td>
                    <td class="py-4 px-6">
                        <div class="flex items-center justify-center gap-3">
                            <button class="text-slate-400 hover:text-indigo-600 transition-colors" onclick="editTimetable(${tt.timetable_id}, '${tt.department}', ${tt.year}, '${tt.day_of_week}', ${tt.period_number}, '${tt.start_time ? tt.start_time.substring(0, 5) : '09:00'}', '${tt.end_time ? tt.end_time.substring(0, 5) : '09:50'}', ${tt.subject}, ${tt.faculty})">
                                <i data-lucide="edit-2" class="w-4 h-4"></i>
                            </button>
                            <button class="text-slate-400 hover:text-red-500 transition-colors" onclick="deleteTimetable(${tt.timetable_id})">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });
        
        if (window.lucide) {
            lucide.createIcons();
        }
    } catch (err) {
        console.error(err);
    }
}

async function deleteTimetable(id) {
    if (!confirm('Are you sure you want to delete this timetable entry?')) return;
    try {
        await api.delete(`/students/timetable/${id}/`);
        utils.showToast('Timetable entry deleted', 'success');
        loadTimetable();
    } catch (err) {
        console.error(err);
        utils.showToast('Error deleting timetable', 'error');
    }
}

window.editTimetable = (id, dept, yr, day, period, start, end, subj, fac) => {
    window.editingTimetableId = id;
    
    document.getElementById('ttDept').value = dept || '';
    document.getElementById('ttYear').value = yr || '';
    document.getElementById('ttDay').value = day || '';
    document.getElementById('ttPeriod').value = period || '';
    document.getElementById('ttStartTime').value = start || '';
    document.getElementById('ttEndTime').value = end || '';
    document.getElementById('ttSubject').value = subj || '';
    document.getElementById('ttFaculty').value = fac || '';
    
    document.querySelector('#addTimetableModalContent h3').innerText = 'Edit Timetable';
    document.querySelector('#addTimetableForm button[type="submit"]').innerText = 'Update';
    
    utils.showModal('addTimetableModal');
}
