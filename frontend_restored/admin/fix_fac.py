path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\admin\faculty.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

missing_html = """                        </svg>
                    </button>
                    <h2 class="text-xl font-extrabold text-slate-800 font-outfit">Faculty Management</h2>
                </div>
            </header>

            <!-- Page Content -->
            <div class="p-8 space-y-6 max-w-7xl w-full mx-auto content-block">
                
                <div class="glass-card p-6 rounded-2xl border border-slate-100 shadow-sm">
                    <!-- Add Actions Row -->
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-lg font-bold text-slate-800 font-outfit">Faculty Members</h3>
                        <div class="flex items-center gap-3 w-full sm:w-auto">
                            <button class="flex items-center justify-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 hover:bg-emerald-100 font-semibold py-2.5 px-4 rounded-xl shadow-sm transition-all" onclick="utils.exportTableToCSV('facultyTable', 'faculty_export.csv')">
                                <i data-lucide="download" class="w-5 h-5"></i><span class="hidden sm:inline">Export</span>
                            </button>
                            <button class="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-550 hover:scale-[1.02] text-white font-semibold py-2.5 px-6 rounded-xl shadow-md transition-all" onclick="utils.showModal('addFacultyModal')">
                                <i data-lucide="plus" class="w-5 h-5"></i><span>Faculty</span>
                            </button>
                        </div>
                    </div>

                    <!-- Faculty Table -->
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse" id="facultyTable">
                            <thead>
                                <tr class="border-b border-slate-200 text-slate-400 text-xs font-semibold uppercase tracking-wider">
                                    <th class="py-3 px-4">Emp ID</th>
                                    <th class="py-3 px-4">Name</th>
                                    <th class="py-3 px-4">Dept</th>
                                    <th class="py-3 px-4">Designation</th>
                                    <th class="py-3 px-4">Email</th>"""

search_str = '                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>\n                                    <th class="py-3 px-4 text-center">Actions</th>'
replace_str = '                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>\n' + missing_html + '\n                                    <th class="py-3 px-4 text-center">Actions</th>'

new_content = content.replace(search_str, replace_str)
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Fixed faculty.html')
