import os
import re

html_file = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\faculty\dashboard.html"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

new_logic = """
            // Load stats
            const fid = user.faculty_id || 1; // Fallback if token is old
            try {
                // Today's classes
                const classes = await api.get(`/faculty/${fid}/today_classes/`);
                const classCount = classes.results ? classes.results.length : (classes.length || 0);
                document.getElementById('kpi-classes').textContent = classCount;

                const container = document.getElementById('todayClasses');
                if (classCount === 0) {
                    container.innerHTML = '<p class="text-center py-10 text-slate-400 text-sm">No classes scheduled for today.</p>';
                } else {
                    const classList = classes.results || classes;
                    container.innerHTML = classList.map(c => `
                        <div class="flex items-center justify-between px-6 py-4 hover:bg-slate-50 transition-colors">
                            <div class="flex items-center gap-4">
                                <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm">P${c.period_number}</div>
                                <div>
                                    <p class="font-semibold text-slate-800">${c.subject_details ? c.subject_details.subject_name : 'Subject '+c.subject}</p>
                                    <p class="text-xs text-slate-400">Year ${c.year} · Section ${c.section}</p>
                                </div>
                            </div>
                            <a href="attendance.html" class="px-4 py-1.5 text-xs font-semibold bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors">Mark Attendance</a>
                        </div>
                    `).join('');
                }

                // Students count
                const students = await api.get(`/faculty/${fid}/students/`);
                const studentCount = students.results ? students.results.length : (students.length || 0);
                document.getElementById('kpi-students').textContent = studentCount;
            } catch(e) {
                console.error(e);
                document.getElementById('todayClasses').innerHTML = '<p class="text-center py-10 text-slate-400 text-sm">Could not load timetable.</p>';
                document.getElementById('kpi-classes').textContent = '0';
                document.getElementById('kpi-students').textContent = '0';
            }

            // Pending leaves
            try {
                const leaves = await api.get('/leave/requests/?status=Pending');
                const leaveCount = leaves.results ? leaves.results.length : (leaves.length || 0);
                document.getElementById('kpi-leaves').textContent = leaveCount;
            } catch(e) {
                console.error(e);
                document.getElementById('kpi-leaves').textContent = '0';
            }
"""

content = re.sub(r'            // Load stats.*?            } catch\(e\) \{\n                document\.getElementById\(\'kpi-leaves\'\)\.textContent = \'0\';\n            \}', new_logic.strip('\n'), content, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
