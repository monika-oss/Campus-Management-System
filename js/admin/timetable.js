// Admin Timetable Logic
let timetableCurrentPage = 1;
const ITEMS_PER_PAGE = 5;

document.addEventListener('DOMContentLoaded', async () => {
    lucide.createIcons();
    if (!auth.checkAuth() || !auth.hasRole('admin')) return;


    loadDepartments();
    loadSubjects();
    loadFaculty();
    loadTimetable();

    // Combobox Setup
    const dropdownBtn = document.getElementById('subjectDropdownBtn');
    const dropdownMenu = document.getElementById('subjectDropdownMenu');
    const searchInput = document.getElementById('subjectSearchInput');
    const addBtn = document.getElementById('subjectAddBtn');
    
    if (dropdownBtn) {
        dropdownBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.classList.toggle('hidden');
            dropdownMenu.classList.toggle('flex');
            if (!dropdownMenu.classList.contains('hidden')) {
                searchInput.focus();
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!dropdownBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.classList.add('hidden');
                dropdownMenu.classList.remove('flex');
            }
        });
        
        searchInput.addEventListener('input', filterSubjectOptions);
        addBtn.addEventListener('click', createNewSubject);
    }

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
            document.getElementById('ttSubject').value = '';
            const subjectDropdownText = document.getElementById('subjectDropdownText');
            if (subjectDropdownText) {
                subjectDropdownText.innerText = 'Select Subject';
                subjectDropdownText.classList.add('text-slate-500');
                subjectDropdownText.classList.remove('text-slate-800');
            }
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

window.allSubjects = [];
async function loadSubjects() {
    try {
        const subjects = await api.get('/students/subjects/');
        window.allSubjects = subjects;
        renderSubjectOptions(subjects);
    } catch (e) {
        console.error(e);
    }
}

function renderSubjectOptions(subjects) {
    const list = document.getElementById('subjectOptionsList');
    if (!list) return;
    
    if (subjects.length === 0) {
        list.innerHTML = '<div class="text-sm text-slate-500 text-center py-4">No subjects found.</div>';
        return;
    }
    
    list.innerHTML = '';
    subjects.forEach(s => {
        list.innerHTML += `
            <div class="flex items-center justify-between px-3 py-2 hover:bg-slate-50 rounded-lg group">
                <div class="flex-1 cursor-pointer" onclick="selectSubject(${s.subject_id}, '${s.subject_name.replace(/'/g, "\\'")}')">
                    <div class="font-medium text-slate-700 text-sm">${s.subject_name}</div>
                    <div class="text-[10px] text-slate-400 mt-0.5">${s.subject_code} &bull; ${s.department_details ? s.department_details.code : ''}</div>
                </div>
                <button type="button" onclick="deleteComboboxSubject(${s.subject_id}, event)" class="p-1.5 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100">
                    <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                </button>
            </div>
        `;
    });
    lucide.createIcons();
}

function filterSubjectOptions(e) {
    const val = e.target.value.toLowerCase().trim();
    const addBtn = document.getElementById('subjectAddBtn');
    
    if (!val) {
        renderSubjectOptions(window.allSubjects);
        addBtn.classList.add('hidden');
        return;
    }
    
    const filtered = window.allSubjects.filter(s => s.subject_name.toLowerCase().includes(val) || s.subject_code.toLowerCase().includes(val));
    renderSubjectOptions(filtered);
    
    const exactMatch = window.allSubjects.find(s => s.subject_name.toLowerCase() === val);
    if (!exactMatch) {
        addBtn.classList.remove('hidden');
    } else {
        addBtn.classList.add('hidden');
    }
}

window.selectSubject = (id, name) => {
    document.getElementById('ttSubject').value = id;
    document.getElementById('subjectDropdownText').innerText = name;
    document.getElementById('subjectDropdownText').classList.remove('text-slate-500');
    document.getElementById('subjectDropdownText').classList.add('text-slate-800');
    
    const menu = document.getElementById('subjectDropdownMenu');
    menu.classList.add('hidden');
    menu.classList.remove('flex');
    
    document.getElementById('subjectSearchInput').value = '';
    filterSubjectOptions({ target: { value: '' } });
};

async function createNewSubject(e) {
    e.stopPropagation();
    const name = document.getElementById('subjectSearchInput').value.trim();
    const dept = document.getElementById('ttDept').value;
    const year = document.getElementById('ttYear').value;
    
    if (!name) return;
    if (!dept) {
        utils.showToast('Please select a Department first', 'warning');
        return;
    }
    
    const btn = document.getElementById('subjectAddBtn');
    btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i>';
    lucide.createIcons();
    
    try {
        const code = name.substring(0, 3).toUpperCase() + Math.floor(100 + Math.random() * 900);
        const newSub = await api.post('/students/subjects/', {
            subject_name: name,
            subject_code: code,
            department: dept,
            year: year || 1,
            credits: 3
        });
        
        utils.showToast('Subject added successfully', 'success');
        await loadSubjects();
        selectSubject(newSub.subject_id, newSub.subject_name);
    } catch (err) {
        console.error(err);
        utils.showToast('Error adding subject', 'error');
    } finally {
        btn.innerText = 'Add';
    }
}

window.deleteComboboxSubject = async (id, e) => {
    e.stopPropagation();
    if (!confirm('Delete this subject? It may affect existing timetables.')) return;
    try {
        await api.delete(`/students/subjects/${id}/`);
        utils.showToast('Subject deleted', 'success');
        
        // If the deleted subject was selected, clear the selection
        if (document.getElementById('ttSubject').value == id) {
            document.getElementById('ttSubject').value = '';
            document.getElementById('subjectDropdownText').innerText = 'Select Subject';
            document.getElementById('subjectDropdownText').classList.add('text-slate-500');
            document.getElementById('subjectDropdownText').classList.remove('text-slate-800');
        }
        
        await loadSubjects();
    } catch (err) {
        console.error(err);
        utils.showToast('Error deleting subject', 'error');
    }
};

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
        utils.showTableSkeleton('#timetableTableBody', 7, 5);
        const timetableList = await api.get('/students/timetable/');
        const tbody = document.getElementById('timetableTableBody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        if (timetableList.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-slate-500">No timetable entries found.</td></tr>`;
            const pg = document.getElementById('timetablePagination');
            if (pg) pg.innerHTML = '';
            return;
        }

        const startIndex = (timetableCurrentPage - 1) * ITEMS_PER_PAGE;
        const paginatedData = timetableList.slice(startIndex, startIndex + ITEMS_PER_PAGE);

        paginatedData.forEach(tt => {
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
        
        utils.renderPagination('timetablePagination', timetableList.length, ITEMS_PER_PAGE, timetableCurrentPage, (newPage) => {
            timetableCurrentPage = newPage;
            loadTimetable();
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
    document.getElementById('ttFaculty').value = fac || '';
    
    // Update Combobox for subject
    document.getElementById('ttSubject').value = subj || '';
    const subjectDropdownText = document.getElementById('subjectDropdownText');
    if (subj && window.allSubjects) {
        const matchingSubject = window.allSubjects.find(s => s.subject_id == subj);
        if (matchingSubject) {
            subjectDropdownText.innerText = matchingSubject.subject_name;
            subjectDropdownText.classList.remove('text-slate-500');
            subjectDropdownText.classList.add('text-slate-800');
        }
    }
    
    document.querySelector('#addTimetableModalContent h3').innerText = 'Edit Timetable';
    document.querySelector('#addTimetableForm button[type="submit"]').innerText = 'Update';
    
    utils.showModal('addTimetableModal');
}

// Subject Management
window.openManageSubjectsModal = async () => {
    utils.showModal('manageSubjectsModal');
    await loadManageSubjectsList();
};

async function loadManageSubjectsList() {
    const list = document.getElementById('manageSubjectsList');
    if (!list) return;
    
    list.innerHTML = '<div class="text-sm text-slate-500 text-center py-4">Loading...</div>';
    try {
        const subjects = await api.get('/students/subjects/');
        if (subjects.length === 0) {
            list.innerHTML = '<div class="text-sm text-slate-500 text-center py-4">No subjects found.</div>';
            return;
        }
        
        list.innerHTML = '';
        subjects.forEach(s => {
            list.innerHTML += `
                <div class="flex items-center justify-between p-3 bg-white border border-slate-100 rounded-xl shadow-sm hover:shadow-md transition-shadow group">
                    <div>
                        <div class="font-semibold text-slate-700 text-sm">${s.subject_name}</div>
                        <div class="text-xs text-slate-500 mt-0.5">${s.subject_code} &bull; ${s.department_details ? s.department_details.code : ''}</div>
                    </div>
                    <button onclick="deleteManageSubject(${s.subject_id})" class="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100">
                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                    </button>
                </div>
            `;
        });
        lucide.createIcons();
    } catch (e) {
        console.error(e);
        list.innerHTML = '<div class="text-sm text-red-500 text-center py-4">Error loading subjects.</div>';
    }
}

document.getElementById('addSubjectForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('newSubjectName').value.trim();
    const dept = document.getElementById('ttDept').value;
    const year = document.getElementById('ttYear').value;
    
    if (!name) return;
    if (!dept) {
        utils.showToast('Please select a Department first', 'error');
        return;
    }
    
    try {
        const code = name.substring(0, 3).toUpperCase() + Math.floor(100 + Math.random() * 900);
        await api.post('/students/subjects/', {
            subject_name: name,
            subject_code: code,
            department: dept,
            year: year || 1,
            credits: 3
        });
        
        document.getElementById('newSubjectName').value = '';
        utils.showToast('Subject added successfully', 'success');
        
        // Reload both lists
        await loadManageSubjectsList();
        await loadSubjects();
    } catch (err) {
        console.error(err);
        utils.showToast('Error adding subject', 'error');
    }
});

window.deleteManageSubject = async (id) => {
    if (!confirm('Are you sure you want to delete this subject? It might affect existing timetables.')) return;
    try {
        await api.delete(`/students/subjects/${id}/`);
        utils.showToast('Subject deleted', 'success');
        
        // Reload both lists
        await loadManageSubjectsList();
        await loadSubjects();
    } catch (err) {
        console.error(err);
        utils.showToast('Error deleting subject', 'error');
    }
};
