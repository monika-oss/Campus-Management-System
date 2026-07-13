// Admin Timetable Logic
document.addEventListener('DOMContentLoaded', async () => {
    lucide.createIcons();
    if (!auth.checkAuth() || !auth.hasRole('admin')) return;

    // GSAP Transitions
    if (window.gsap) {
        gsap.to("#topNavbar", { duration: 0.8, opacity: 1, ease: "power2.out", delay: 0.2 });
        gsap.to(".content-block", { duration: 0.8, opacity: 1, y: 0, ease: "power3.out", delay: 0.3 });
    }

    // Sidebar Collapsible Toggle
    const sidebar = document.getElementById('adminSidebar') || document.getElementById('studentSidebar') || document.getElementById('facultySidebar');
    const toggleBtn = document.getElementById('sidebarToggle');
    if (sidebar && toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            if (window.innerWidth < 1024) {
                sidebar.classList.toggle('-translate-x-full');
            } else {
                sidebar.classList.toggle('collapsed-sidebar');
            }
        });
    }
    const closeBtn = document.getElementById('closeSidebar');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            if(sidebar) sidebar.classList.add('-translate-x-full');
        });
    }

    loadDepartments();
    loadSubjects();
    loadFaculty();
    loadTimetable();

    document.getElementById('filterDept')?.addEventListener('change', loadTimetable);
    document.getElementById('filterYear')?.addEventListener('change', loadTimetable);
    document.getElementById('filterDay')?.addEventListener('change', loadTimetable);

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
                let errMsg = 'Error saving timetable';
                if (err && err.data) {
                    if (err.data.non_field_errors && err.data.non_field_errors.length > 0) {
                        errMsg = err.data.non_field_errors[0];
                    } else if (typeof err.data === 'object') {
                        const vals = Object.values(err.data);
                        if (vals.length > 0 && Array.isArray(vals[0])) {
                            errMsg = vals[0][0];
                        } else if (vals.length > 0 && typeof vals[0] === 'string') {
                            errMsg = vals[0];
                        }
                    }
                }
                utils.showToast(errMsg, 'error');
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

let globalDepartmentsData = [];

async function loadDepartments() {
    try {
        const departments = await api.get('/students/departments/');
        globalDepartmentsData = departments;
        const select = document.getElementById('ttDept');
        const filterSelect = document.getElementById('filterDept');
        
        if (select) {
            select.innerHTML = '<option value="">Select Dept</option>';
            departments.forEach(d => {
                select.innerHTML += `<option value="${d.id}">${d.name} (${d.code})</option>`;
            });
        }
        
        if (filterSelect) {
            filterSelect.innerHTML = '<option value="">All Depts</option>';
            departments.forEach(d => {
                filterSelect.innerHTML += `<option value="${d.id}">${d.name} (${d.code})</option>`;
            });
        }
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

let timetableData = [];
let timetableCurrentPage = 1;
const ITEMS_PER_PAGE = 6;

async function loadTimetable() {
    try {
        utils.showTableSkeleton('#timetableTableBody', 7, ITEMS_PER_PAGE);
        const dept = document.getElementById('filterDept')?.value || '';
        const year = document.getElementById('filterYear')?.value || '';
        const day = document.getElementById('filterDay')?.value || '';
        
        let url = '/students/timetable/?';
        if (dept) url += `department=${dept}&`;
        if (year) url += `year=${year}&`;
        if (day) url += `day_of_week=${day}&`;
        
        timetableData = await api.get(url);
        timetableCurrentPage = 1;
        renderTimetableTable();
    } catch (err) {
        console.error(err);
    }
}

function renderTimetableTable() {
    const tbody = document.getElementById('timetableTableBody');
    if (!tbody) return;
    
    if (timetableData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-8 text-slate-500">No timetable entries found.</td></tr>`;
        const pagContainer = document.getElementById('timetablePagination');
        if(pagContainer) pagContainer.innerHTML = '';
        return;
    }

    const paginated = utils.paginateData(timetableData, timetableCurrentPage, ITEMS_PER_PAGE);
    
    tbody.innerHTML = paginated.map((tt, index) => {
        const deptObj = globalDepartmentsData.find(d => d.id == tt.department);
        const deptDisplay = deptObj ? deptObj.code : tt.department;
        const isLastRows = index >= paginated.length - 2 && paginated.length > 2;
        const dropdownClasses = isLastRows ? 'bottom-full mb-1 origin-bottom-right' : 'mt-1 origin-top-right';
        
        return `
        <tr class="hover:bg-slate-50/50 transition-colors">
            <td class="py-4 px-6 text-slate-700 font-medium">${tt.day_of_week}</td>
            <td class="py-4 px-6 text-slate-600">Period ${tt.period_number}</td>
            <td class="py-4 px-6 text-slate-600"><span class="bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-md text-xs font-semibold">${tt.start_time ? tt.start_time.substring(0, 5) : '09:00'} - ${tt.end_time ? tt.end_time.substring(0, 5) : '09:50'}</span></td>
            <td class="py-4 px-6 text-slate-600">Yr ${tt.year}</td>
            <td class="py-4 px-6 text-slate-600">${deptDisplay}</td>
            <td class="py-4 px-6 text-slate-600">${tt.subject_details ? tt.subject_details.subject_name : 'Subject ' + tt.subject}</td>
            <td class="py-4 px-6 text-slate-600">${tt.faculty_name || 'Faculty ' + tt.faculty}</td>
            <td class="py-4 px-6 text-center">
                <div class="relative inline-block text-left group/menu z-10 hover:z-50">
                    <button class="p-1.5 px-2 bg-slate-50 text-slate-600 border border-slate-200 hover:bg-slate-200 rounded-lg transition-colors shadow-sm focus:outline-none">
                        <i class="bi bi-three-dots-vertical"></i>
                    </button>
                    <div class="absolute right-0 ${dropdownClasses} w-28 bg-white border border-slate-100 rounded-xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.1)] opacity-0 invisible group-hover/menu:opacity-100 group-hover/menu:visible transition-all z-[60] flex flex-col p-1.5 scale-95 group-hover/menu:scale-100">
                        <button class="flex items-center gap-2.5 px-3 py-2 text-sm font-medium text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors text-left w-full" onclick="viewTimetable(${tt.timetable_id})">
                            <i class="bi bi-eye"></i> View
                        </button>
                        <button class="flex items-center gap-2.5 px-3 py-2 text-sm font-medium text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors text-left w-full" onclick="editTimetable(${tt.timetable_id}, '${tt.department}', ${tt.year}, '${tt.day_of_week}', ${tt.period_number}, '${tt.start_time ? tt.start_time.substring(0, 5) : '09:00'}', '${tt.end_time ? tt.end_time.substring(0, 5) : '09:50'}', ${tt.subject}, ${tt.faculty})">
                            <i class="bi bi-pencil-square"></i> Edit
                        </button>
                        <button class="flex items-center gap-2.5 px-3 py-2 text-sm font-medium text-rose-600 hover:bg-rose-50 rounded-lg transition-colors text-left w-full" onclick="deleteTimetable(${tt.timetable_id})">
                            <i class="bi bi-trash"></i> Delete
                        </button>
                    </div>
                </div>
            </td>
        </tr>
    `;
    }).join('');
    
    if (window.lucide) {
        lucide.createIcons();
    }
    
    utils.renderPagination('timetablePagination', timetableData.length, ITEMS_PER_PAGE, timetableCurrentPage, (newPage) => {
        timetableCurrentPage = newPage;
        renderTimetableTable();
    });
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

window.viewTimetable = function(id) {
    const tt = timetableData.find(t => t.timetable_id == id);
    if(tt) utils.showViewModal('Timetable Details', tt);
};

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
