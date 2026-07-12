import re

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\faculty\attendance.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# I will replace everything from `<script>` to `</script>`
start = html.find('<script>')
end = html.rfind('</script>') + 9

new_script = """<script>
        document.addEventListener('DOMContentLoaded', () => {
            if(!auth.checkAuth()) return;
            const user = auth.getCurrentUser();
            
            // Set user info
            document.querySelectorAll('.faculty-name').forEach(el => el.textContent = user.name || 'Faculty');
            document.querySelectorAll('.faculty-id').forEach(el => el.textContent = user.employee_id || '');
            
            // Highlight current nav
            document.querySelectorAll('.nav-item').forEach(el => {
                if(el.getAttribute('href').includes('attendance.html')) {
                    el.classList.add('active');
                }
            });

            // Set today's date in input
            const todayStr = new Date().toISOString().split('T')[0];
            document.getElementById('attDate').value = todayStr;
            document.getElementById('attDate').max = todayStr;
            
            let currentStudents = [];
            
            // Load today's classes
            loadTodayClasses(user.id);
            
            async function loadTodayClasses(facultyId) {
                try {
                    const classes = await api.get(`/faculty/${facultyId}/today_classes/`);
                    const select = document.getElementById('attSubject');
                    if(classes.length === 0) {
                        select.innerHTML = '<option value="">No classes scheduled for today</option>';
                    } else {
                        classes.forEach(c => {
                            const name = c.subject_details ? c.subject_details.subject_name : 'Sub '+c.subject;
                            select.innerHTML += `<option value="${c.subject}" data-dept="${c.department}" data-year="${c.year}" data-sec="${c.section}">Period ${c.period_number} - ${name} (${c.year} Yr, Sec ${c.section})</option>`;
                        });
                    }
                } catch(e) {
                    console.error(e);
                }
            }
            
            document.getElementById('attendanceFilterForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const subjSelect = document.getElementById('attSubject');
                if(!subjSelect.value) return utils.showToast('Select a class', 'error');
                
                const opt = subjSelect.options[subjSelect.selectedIndex];
                const dept = opt.dataset.dept;
                const year = opt.dataset.year;
                const sec = opt.dataset.sec;
                
                try {
                    let url = `/students/?department=${dept}&year=${year}`;
                    if (sec && sec !== 'null' && sec !== 'None') url += `&section=${sec}`;
                    const students = await api.get(url);
                    
                    const list = document.getElementById('studentsList');
                    list.innerHTML = '';
                    currentStudents = students;
                    
                    if (students.length === 0) {
                        list.innerHTML = '<p class="text-center py-8 text-slate-400">No students found.</p>';
                    } else {
                        students.forEach(s => {
                            let studentId = s.student_id || s.id;
                            list.innerHTML += `
                                <div class="flex items-center justify-between p-4 hover:bg-slate-50/50 transition-colors">
                                    <div class="flex items-center gap-4">
                                        <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm">
                                            ${s.name.substring(0,2).toUpperCase()}
                                        </div>
                                        <div>
                                            <h4 class="font-bold text-slate-800">${s.name}</h4>
                                            <p class="text-xs text-slate-500">${s.roll_number}</p>
                                        </div>
                                    </div>
                                    <div class="flex gap-2">
                                        <label class="att-radio">
                                            <input type="radio" name="att_${studentId}" value="present" checked>
                                            <div class="radio-btn">P</div>
                                        </label>
                                        <label class="att-radio">
                                            <input type="radio" name="att_${studentId}" value="absent">
                                            <div class="radio-btn">A</div>
                                        </label>
                                        <label class="att-radio">
                                            <input type="radio" name="att_${studentId}" value="leave">
                                            <div class="radio-btn">L</div>
                                        </label>
                                        <label class="att-radio">
                                            <input type="radio" name="att_${studentId}" value="onduty">
                                            <div class="radio-btn">OD</div>
                                        </label>
                                    </div>
                                </div>
                            `;
                        });
                    }
                    
                    document.getElementById('attendanceContainer').classList.remove('hidden');
                } catch(err) {
                    console.error(err);
                    utils.showToast('Error loading students', 'error');
                }
            });
            
            document.getElementById('attendanceSubmitForm').addEventListener('submit', async(e) => {
                e.preventDefault();
                const subject_id = document.getElementById('attSubject').value;
                const period_number = document.getElementById('attPeriod').value;
                const date = document.getElementById('attDate').value;
                
                const attendances = [];
                currentStudents.forEach(s => {
                    let studentId = s.student_id || s.id;
                    const status = document.querySelector(`input[name="att_${studentId}"]:checked`).value;
                    attendances.push({ student_id: studentId, status: status });
                });
                
                try {
                    await api.post('/attendance/mark/', {
                        subject_id, date, period_number, attendances
                    });
                    utils.showToast('Attendance marked successfully!', 'success');
                    document.getElementById('attendanceContainer').classList.add('hidden');
                } catch(err) {
                    console.error(err);
                    utils.showToast('Error marking attendance', 'error');
                }
            });
        });
        
        window.markAll = function(status) {
            document.querySelectorAll(`input[value="${status}"]`).forEach(input => {
                input.checked = true;
            });
        };
    </script>"""

if start != -1 and end != -1:
    new_html = html[:start] + new_script + html[end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print('Fixed successfully!')
else:
    print('Could not find script block')
