// Inject Global Scrollbar Styling
const scrollbarStyle = document.createElement('style');
scrollbarStyle.innerHTML = `
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
  ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
  * { scrollbar-width: thin !important; scrollbar-color: #cbd5e1 transparent !important; }
`;
document.head.appendChild(scrollbarStyle);

const utils = {
  showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.position = 'fixed';
      container.style.top = '20px';
      container.style.right = '20px';
      container.style.zIndex = '9999';
      document.body.appendChild(container);
      
      const style = document.createElement('style');
      style.innerHTML = `
        .toast {
          background-color: #ffffff;
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
          padding: 12px 20px;
          margin-bottom: 12px;
          display: flex;
          align-items: center;
          gap: 12px;
          transform: translateX(120%);
          transition: transform 0.3s ease;
          min-width: 280px;
          border: 1px solid #e2e8f0;
        }
        .toast.show {
          transform: translateX(0);
        }
        .toast.success { background-color: #ecfdf5; border-left: 4px solid #10b981; border-color: #d1fae5; border-left-color: #10b981; }
        .toast.error { background-color: #fef2f2; border-left: 4px solid #ef4444; border-color: #fee2e2; border-left-color: #ef4444; }
        .toast.warning { background-color: #fffbeb; border-left: 4px solid #f59e0b; border-color: #fef3c7; border-left-color: #f59e0b; }
        .toast.info { background-color: #eff6ff; border-left: 4px solid #3b82f6; border-color: #dbeafe; border-left-color: #3b82f6; }
        .toast-icon { font-size: 20px; }
        .toast.success .toast-message { color: #065f46; }
        .toast.error .toast-message { color: #991b1b; }
        .toast.warning .toast-message { color: #92400e; }
        .toast.info .toast-message { color: #1e40af; }
        .toast-message { font-weight: 500; font-family: 'Inter', sans-serif; font-size: 14px; }
      `;
      document.head.appendChild(style);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';
    if (type === 'warning') icon = '⚠️';

    toast.innerHTML = `
      <div class="toast-icon">${icon}</div>
      <div class="toast-message">${message}</div>
    `;

    container.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  },

  showModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
      modal.classList.remove('hidden');
      modal.classList.add('active');
    }
  },

  hideModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('active');
    }
  },

  togglePasswordVisibility(inputId, button, e) {
      if (e) {
          e.stopPropagation();
          e.preventDefault();
      }
      const input = document.getElementById(inputId);
      if (input) {
          const isPassword = input.type === 'password';
          input.type = isPassword ? 'text' : 'password';
          
          button.innerHTML = `<i data-lucide="${isPassword ? 'eye' : 'eye-off'}" class="w-4 h-4"></i>`;
          if (window.lucide) {
              lucide.createIcons({node: button});
          }
      }
  },



  formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-GB'); // DD/MM/YYYY
  },

  formatDateTime(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    const datePart = date.toLocaleDateString('en-GB');
    const timePart = date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    return `${datePart} ${timePart}`;
  },

  debounce(func, delay) {
    let timeoutId;
    return function (...args) {
      if (timeoutId) clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        func.apply(this, args);
      }, delay);
    };
  },

  paginateData(data, currentPage, itemsPerPage) {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return data.slice(startIndex, startIndex + itemsPerPage);
  },

  renderPagination(containerId, totalItems, itemsPerPage, currentPage, onPageChangeCallback) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = '';
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    
    if (totalItems === 0) return; // No pagination needed if empty

    // Previous Button
    const prevBtn = document.createElement('button');
    prevBtn.innerHTML = 'Previous';
    prevBtn.className = `px-3 py-1 border rounded-md text-sm font-medium transition-colors ${currentPage === 1 ? 'bg-slate-50 text-slate-400 border-slate-200 cursor-not-allowed' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}`;
    prevBtn.disabled = currentPage === 1;
    prevBtn.onclick = () => { if (currentPage > 1) onPageChangeCallback(currentPage - 1); };
    container.appendChild(prevBtn);

    // Page Numbers
    const pageWrapper = document.createElement('div');
    pageWrapper.className = 'flex items-center gap-1';
    
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);
    
    if (startPage > 1) {
        const firstPageBtn = document.createElement('button');
        firstPageBtn.textContent = '1';
        firstPageBtn.className = 'px-3 py-1 border border-slate-300 rounded-md text-sm font-medium bg-white text-slate-700 hover:bg-slate-50';
        firstPageBtn.onclick = () => onPageChangeCallback(1);
        pageWrapper.appendChild(firstPageBtn);
        if (startPage > 2) {
            const ellipsis = document.createElement('span');
            ellipsis.textContent = '...';
            ellipsis.className = 'px-2 text-slate-400';
            pageWrapper.appendChild(ellipsis);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.className = `px-3 py-1 border rounded-md text-sm font-medium transition-colors ${currentPage === i ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}`;
        btn.onclick = () => onPageChangeCallback(i);
        pageWrapper.appendChild(btn);
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            const ellipsis = document.createElement('span');
            ellipsis.textContent = '...';
            ellipsis.className = 'px-2 text-slate-400';
            pageWrapper.appendChild(ellipsis);
        }
        const lastPageBtn = document.createElement('button');
        lastPageBtn.textContent = totalPages;
        lastPageBtn.className = 'px-3 py-1 border border-slate-300 rounded-md text-sm font-medium bg-white text-slate-700 hover:bg-slate-50';
        lastPageBtn.onclick = () => onPageChangeCallback(totalPages);
        pageWrapper.appendChild(lastPageBtn);
    }
    
    container.appendChild(pageWrapper);

    // Next Button
    const nextBtn = document.createElement('button');
    nextBtn.innerHTML = 'Next';
    nextBtn.className = `px-3 py-1 border rounded-md text-sm font-medium transition-colors ${currentPage === totalPages ? 'bg-slate-50 text-slate-400 border-slate-200 cursor-not-allowed' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}`;
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.onclick = () => { if (currentPage < totalPages) onPageChangeCallback(currentPage + 1); };
    container.appendChild(nextBtn);
  },

  confirmAction(message, onConfirm) {
    const fireSwal = () => {
      Swal.fire({
        text: message,
        showCancelButton: true,
        confirmButtonColor: '#2563eb',
        cancelButtonColor: '#64748b',
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        icon: undefined,
        customClass: {
          confirmButton: 'bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 font-medium',
          cancelButton: 'bg-slate-500 hover:bg-slate-600 text-white rounded-lg px-4 py-2 font-medium ml-3'
        },
        buttonsStyling: false
      }).then((result) => {
        if (result.isConfirmed) {
          onConfirm();
        }
      });
    };

    if (typeof Swal === 'undefined') {
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11';
      script.onload = fireSwal;
      document.head.appendChild(script);
    } else {
      fireSwal();
    }
  },

  exportCSV(data, filename) {
    if (!data || !data.length) return;
    
    const keys = Object.keys(data[0]);
    const csvContent = [
      keys.join(','),
      ...data.map(row => keys.map(k => `"${row[k] || ''}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', filename);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  },

  gradeFromMarks(marks) {
    if (marks >= 90) return { grade: 'A+', class: 'badge-success' };
    if (marks >= 80) return { grade: 'A', class: 'badge-success' };
    if (marks >= 70) return { grade: 'B+', class: 'badge-info' };
    if (marks >= 60) return { grade: 'B', class: 'badge-info' };
    if (marks >= 50) return { grade: 'C', class: 'badge-warning' };
    if (marks >= 40) return { grade: 'D', class: 'badge-warning' };
    return { grade: 'F', class: 'badge-danger' };
  }
};

// Global event listeners for modals
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('active');
    e.target.classList.add('hidden');
  }
  if (e.target.classList.contains('modal-close') || e.target.closest('.modal-close')) {
    const modal = e.target.closest('.modal-overlay');
    if (modal) {
      modal.classList.remove('active');
      modal.classList.add('hidden');
    }
  }
});


document.addEventListener('DOMContentLoaded', () => {
    // Add notification-badge class to the span inside #bellNotify dynamically
    document.querySelectorAll('#bellNotify span').forEach(span => {
        span.classList.add('notification-badge');
    });

    // Profile Dropdown logic
    const avatar = document.getElementById('userAvatar');
    if (avatar && typeof auth !== 'undefined' && auth.checkAuth()) {
        const parent = avatar.parentElement;
        parent.classList.add('relative');
        
        // Create Dropdown Element
        const dropdown = document.createElement('div');
        dropdown.id = 'profileDropdown';
        dropdown.className = 'absolute right-0 mt-3 w-64 bg-white rounded-2xl shadow-xl border border-slate-100 hidden z-50 p-4 transition-all duration-200 transform scale-95 opacity-0 origin-top-right';
        dropdown.style.top = '100%';
        parent.appendChild(dropdown);
        
        const user = auth.getUser() || {};
        const roleName = user.role ? user.role.charAt(0).toUpperCase() + user.role.slice(1) : 'User';

        window.renderProfileDropdown = function(view = 'details', event = null) {
            if (event) {
                event.stopPropagation();
                event.preventDefault();
            }
            if (view === 'details') {
                let detailsHTML = '';
                if (user.role === 'student') {
                    detailsHTML = `
                        <div class="mt-2.5">
                            <p class="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Register Number</p>
                            <p class="text-sm font-semibold text-slate-700 mt-0.5">${user.roll_number || 'N/A'}</p>
                        </div>
                    `;
                } else if (user.role === 'faculty') {
                    detailsHTML = `
                        <div class="mt-2.5">
                            <p class="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Faculty ID</p>
                            <p class="text-sm font-semibold text-slate-700 mt-0.5">${user.faculty_id || 'N/A'}</p>
                        </div>
                    `;
                } else {
                    detailsHTML = `
                        <div class="mt-2.5">
                            <p class="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Username</p>
                            <p class="text-sm font-semibold text-slate-700 mt-0.5">${user.username || 'admin'}</p>
                        </div>
                    `;
                }

                dropdown.innerHTML = `
                    <div class="flex items-center gap-3 pb-3 border-b border-slate-100">
                        <div class="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-sm">
                            ${(user.name || 'U')[0].toUpperCase()}
                        </div>
                        <div class="min-w-0 flex-1">
                            <h4 class="font-bold text-slate-800 text-sm truncate">${user.name || 'User'}</h4>
                            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-100 mt-0.5">${roleName}</span>
                        </div>
                    </div>
                    <div class="py-3 flex flex-col items-start text-left">
                        <div class="w-full text-left">
                            <p class="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Email</p>
                            <p class="text-sm font-semibold text-slate-700 mt-0.5 truncate w-full">${user.email || 'N/A'}</p>
                        </div>
                        <div class="w-full text-left">
                            ${detailsHTML}
                        </div>
                    </div>
                    <div class="pt-3 border-t border-slate-100 space-y-2">
                        <button onclick="renderProfileDropdown('reset', event)" class="w-full flex items-center justify-center gap-2 bg-slate-50 hover:bg-blue-50 hover:text-blue-600 text-slate-700 py-2.5 rounded-xl transition-all font-semibold border border-slate-200 hover:border-blue-200 shadow-sm text-sm">
                            <i data-lucide="key-round" class="w-4 h-4 text-blue-500"></i> Reset Password
                        </button>
                        <button onclick="auth.logout()" class="w-full flex items-center justify-center gap-2 bg-slate-50 hover:bg-rose-50 hover:text-rose-600 text-slate-700 py-2.5 rounded-xl transition-all font-semibold border border-slate-200 hover:border-rose-200 shadow-sm text-sm">
                            <i data-lucide="log-out" class="w-4 h-4 text-rose-500"></i> Logout
                        </button>
                    </div>
                `;
            } else if (view === 'reset') {
                dropdown.innerHTML = `
                    <div class="space-y-3 text-left">
                        <div class="flex items-center gap-2 pb-2 border-b border-slate-100">
                            <button onclick="renderProfileDropdown('details', event)" class="p-1 hover:bg-slate-100 text-slate-400 hover:text-slate-600 rounded-lg transition-all">
                                <i data-lucide="arrow-left" class="w-4 h-4"></i>
                            </button>
                            <h4 class="font-bold text-slate-800 text-sm">Reset Password</h4>
                        </div>
                        <form id="resetPasswordFormInline" class="space-y-3">
                            <div>
                                <label class="block text-[10px] font-semibold text-slate-400 uppercase tracking-wider">New Password</label>
                                <div class="relative">
                                    <input type="password" id="resetNewPassword" class="w-full pl-3 pr-10 py-1.5 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-xs font-medium" placeholder="••••••••" required>
                                    <button type="button" onclick="utils.togglePasswordVisibility('resetNewPassword', this, event)" class="absolute right-2.5 top-1.5 text-slate-400 hover:text-slate-600 focus:outline-none">
                                        <i data-lucide="eye-off" class="w-4 h-4"></i>
                                    </button>
                                </div>
                            </div>
                            <div>
                                <label class="block text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Confirm Password</label>
                                <div class="relative">
                                    <input type="password" id="resetConfirmPassword" class="w-full pl-3 pr-10 py-1.5 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-xs font-medium" placeholder="••••••••" required>
                                    <button type="button" onclick="utils.togglePasswordVisibility('resetConfirmPassword', this, event)" class="absolute right-2.5 top-1.5 text-slate-400 hover:text-slate-600 focus:outline-none">
                                        <i data-lucide="eye-off" class="w-4 h-4"></i>
                                    </button>
                                </div>
                            </div>
                            <button type="submit" class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-md shadow-blue-500/20 transition-all flex items-center justify-center gap-1.5">
                                Submit Reset
                            </button>
                        </form>
                    </div>
                `;

                // Handle inline form submit
                document.getElementById('resetPasswordFormInline').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const newPassword = document.getElementById('resetNewPassword').value;
                    const confirmPassword = document.getElementById('resetConfirmPassword').value;
                    
                    if (newPassword !== confirmPassword) {
                        return utils.showToast('Passwords do not match', 'error');
                    }
                    
                    try {
                        const btn = e.target.querySelector('button[type="submit"]');
                        btn.disabled = true;
                        btn.innerHTML = '<span class="animate-spin border-2 border-white border-t-transparent rounded-full w-3 h-3 mr-1.5"></span> Updating...';
                        
                        await api.post('/auth/change-password/', { new_password: newPassword });
                        utils.showToast('Password reset successfully!', 'success');
                        
                        // Close dropdown
                        dropdown.classList.remove('opacity-100', 'scale-100');
                        dropdown.classList.add('opacity-0', 'scale-95');
                        setTimeout(() => {
                            dropdown.classList.add('hidden');
                            renderProfileDropdown('details');
                        }, 200);
                    } catch(err) {
                        console.error(err);
                        utils.showToast(err.message || 'Failed to reset password', 'error');
                    } finally {
                        const btn = e.target.querySelector('button[type="submit"]');
                        if (btn) {
                            btn.disabled = false;
                            btn.innerHTML = 'Submit Reset';
                        }
                    }
                });
            }
            if(window.lucide) lucide.createIcons({node: dropdown});
        };

        // Render default view
        renderProfileDropdown('details');
        
        avatar.addEventListener('click', (e) => {
            e.stopPropagation();
            const isHidden = dropdown.classList.contains('hidden');
            if (isHidden) {
                dropdown.classList.remove('hidden');
                setTimeout(() => {
                    dropdown.classList.remove('opacity-0', 'scale-95');
                    dropdown.classList.add('opacity-100', 'scale-100');
                }, 10);
            } else {
                dropdown.classList.remove('opacity-100', 'scale-100');
                dropdown.classList.add('opacity-0', 'scale-95');
                setTimeout(() => dropdown.classList.add('hidden'), 200);
            }
        });
        
        document.addEventListener('click', (event) => {
            if (!dropdown.contains(event.target) && event.target !== avatar) {
                dropdown.classList.remove('opacity-100', 'scale-100');
                dropdown.classList.add('opacity-0', 'scale-95');
                setTimeout(() => dropdown.classList.add('hidden'), 200);
            }
        });
    }

    document.querySelectorAll('.sidebar-item-link').forEach(link => {
        link.addEventListener('click', function() {
            document.querySelectorAll('.sidebar-item-link').forEach(l => {
                l.classList.remove('bg-blue-600', 'text-white', 'shadow-md', 'shadow-blue-600/20');
                l.classList.add('text-slate-200');
            });
            this.classList.remove('text-slate-200', 'hover:bg-slate-800');
            this.classList.add('bg-blue-600', 'text-white', 'shadow-md', 'shadow-blue-600/20');
        });
    });
});

// Global Notification Drawer
const NotificationDrawer = {
  isOpen: false,
  notifications: [],
  activeTab: 'unread',
  
  init() {
    if (document.getElementById('notification-drawer')) return;
    
    const overlay = document.createElement('div');
    overlay.id = 'nd-overlay';
    overlay.className = 'fixed inset-0 bg-black bg-opacity-40 backdrop-blur-sm z-40 hidden transition-opacity opacity-0';
    overlay.onclick = () => this.close();
    
    const drawer = document.createElement('div');
    drawer.id = 'notification-drawer';
    drawer.className = 'fixed top-0 right-0 h-full w-full max-w-sm bg-white shadow-2xl z-50 transform translate-x-full transition-transform duration-300 flex flex-col font-sans';
    
    drawer.innerHTML = `
      <div class="px-5 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
        <h2 class="text-lg font-bold text-slate-800 flex items-center gap-2">
          <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
          Notifications
        </h2>
        <button onclick="NotificationDrawer.close()" class="text-slate-400 hover:text-slate-600 bg-white hover:bg-slate-100 rounded-full p-1.5 transition-colors focus:outline-none">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
      
      <div class="px-5 py-2 border-b border-slate-100 flex gap-4 text-sm font-semibold">
        <button id="nd-tab-unread" onclick="NotificationDrawer.setTab('unread')" class="pb-2 border-b-2 border-blue-600 text-blue-600 transition-colors">Unread (<span id="nd-unread-count">0</span>)</button>
        <button id="nd-tab-read" onclick="NotificationDrawer.setTab('read')" class="pb-2 border-b-2 border-transparent text-slate-500 hover:text-slate-700 transition-colors">Read</button>
      </div>
      
      <div class="px-4 py-2 border-b border-slate-100 bg-slate-50 flex items-center justify-between text-xs">
        <div class="flex items-center gap-2">
            <input type="checkbox" id="nd-select-all" onclick="NotificationDrawer.toggleSelectAll(this.checked)" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500 cursor-pointer w-3.5 h-3.5">
            <label for="nd-select-all" class="font-semibold text-slate-600 cursor-pointer">Select All</label>
        </div>
        <div class="flex gap-2">
            <button onclick="NotificationDrawer.markSelectedRead()" class="text-slate-500 hover:text-blue-600 p-1 rounded hover:bg-blue-50 transition-colors" title="Mark selected as read">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </button>
            <button onclick="NotificationDrawer.deleteSelected()" class="text-slate-500 hover:text-red-600 p-1 rounded hover:bg-red-50 transition-colors" title="Delete selected">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            </button>
        </div>
      </div>

      
      <div id="nd-content" class="flex-1 overflow-y-auto bg-slate-50/50 p-3 space-y-2">
        <div class="text-center py-10 text-slate-400 text-sm">Loading...</div>
      </div>
    `;
    
    document.body.appendChild(overlay);
    document.body.appendChild(drawer);
  },
  
  open() {
    this.init();
    const overlay = document.getElementById('nd-overlay');
    const drawer = document.getElementById('notification-drawer');
    overlay.classList.remove('hidden');
    setTimeout(() => {
      overlay.classList.remove('opacity-0');
      drawer.classList.remove('translate-x-full');
    }, 10);
    this.isOpen = true;
    this.fetchNotifications();
  },
  
  close() {
    const overlay = document.getElementById('nd-overlay');
    const drawer = document.getElementById('notification-drawer');
    if(!drawer) return;
    overlay.classList.add('opacity-0');
    drawer.classList.add('translate-x-full');
    setTimeout(() => overlay.classList.add('hidden'), 300);
    this.isOpen = false;
  },
  
  toggle() {
    this.isOpen ? this.close() : this.open();
  },
  
  setTab(tab) {
    this.activeTab = tab;
    document.getElementById('nd-tab-unread').className = tab === 'unread' ? 'pb-2 border-b-2 border-blue-600 text-blue-600 transition-colors' : 'pb-2 border-b-2 border-transparent text-slate-500 hover:text-slate-700 transition-colors';
    document.getElementById('nd-tab-read').className = tab === 'read' ? 'pb-2 border-b-2 border-blue-600 text-blue-600 transition-colors' : 'pb-2 border-b-2 border-transparent text-slate-500 hover:text-slate-700 transition-colors';
    this.render();
  },
  
  async fetchNotifications() {
    try {
      const data = await api.get('/notifications/');
      this.notifications = Array.isArray(data) ? data : (data.results || []);
      this.updateCounters();
      this.render();
    } catch (e) {
      document.getElementById('nd-content').innerHTML = '<div class="text-center py-10 text-red-400 text-sm">Failed to load</div>';
    }
  },
  
  updateCounters() {
    const unreadCount = this.notifications.filter(n => !n.is_read).length;
    document.getElementById('nd-unread-count').textContent = unreadCount;
    NotificationService.updateBadge(unreadCount);
  },
  
  render() {
    const content = document.getElementById('nd-content');
    const filtered = this.notifications.filter(n => this.activeTab === 'unread' ? !n.is_read : n.is_read);
    
    if (filtered.length === 0) {
      content.innerHTML = `
        <div class="flex flex-col items-center justify-center py-12 text-slate-400">
          <svg class="w-12 h-12 mb-3 text-slate-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
          <span class="text-sm font-medium">No ${this.activeTab} notifications</span>
        </div>
      `;
      return;
    }
    
    content.innerHTML = filtered.map(n => {
      let icon = '<div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg></div>';
      if(n.notification_type === 'success') icon = '<div class="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg></div>';
      if(n.notification_type === 'warning') icon = '<div class="w-8 h-8 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg></div>';
      if(n.notification_type === 'error') icon = '<div class="w-8 h-8 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg></div>';
      
      const timeStr = utils.formatDateTime(n.created_at);
      
      return `
        <div class="bg-white p-3 rounded-lg shadow-sm border border-slate-100 relative group hover:border-blue-200 transition-colors">
          <div class="flex gap-3 items-start">
            <div class="pt-1">
                <input type="checkbox" value="${n.notification_id}" class="nd-checkbox rounded border-slate-300 text-blue-600 focus:ring-blue-500 cursor-pointer w-4 h-4" onchange="NotificationDrawer.updateSelectAllCheckbox()">
            </div>
            ${icon}
            <div class="flex-1 min-w-0">
              <h4 class="text-sm font-bold text-slate-800 truncate">${n.title}</h4>
              <p class="text-xs text-slate-600 mt-1 line-clamp-2">${n.description}</p>
              <div class="text-[10px] text-slate-400 mt-2 font-medium">${timeStr}</div>
            </div>
          </div>
          
          <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col gap-1">
            ${!n.is_read ? `<button onclick="NotificationDrawer.markRead(${n.notification_id})" class="p-1.5 bg-slate-50 hover:bg-blue-50 text-blue-600 rounded-md transition-colors" title="Mark as read"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg></button>` : ''}
            <button onclick="NotificationDrawer.deleteSingle(${n.notification_id})" class="p-1.5 bg-slate-50 hover:bg-red-50 text-red-500 rounded-md transition-colors" title="Delete"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg></button>
          </div>
        </div>
      `;
    }).join('');
  },
  
  async markRead(id) {
    try {
      await api.post(`/notifications/${id}/read/`, {});
      const notif = this.notifications.find(n => n.notification_id === id);
      if (notif) notif.is_read = true;
      this.updateCounters();
      this.render();
    } catch(e) {
      console.error(e);
    }
  },
  
  async deleteSingle(id) {
    try {
      await api.post(`/notifications/${id}/hide/`, {});
      this.notifications = this.notifications.filter(n => n.notification_id !== id);
      this.updateCounters();
      this.render();
    } catch(e) {
      console.error(e);
    }
  },
  
  async markAllRead() {
    try {
      await api.post('/notifications/mark_all_read/', {});
      this.notifications.forEach(n => n.is_read = true);
      this.updateCounters();
      this.render();
      utils.showToast('All marked as read', 'success');
    } catch(e) {
      console.error(e);
    }
  },
  
  async deleteAll() {
    if(!confirm("Are you sure you want to clear all notifications?")) return;
    try {
      await api.post('/notifications/delete_all/', {});
      this.notifications = [];
      this.updateCounters();
      this.render();
      utils.showToast('All notifications cleared', 'success');
    } catch(e) {
      console.error(e);
    }
  },
  
  toggleSelectAll(checked) {
    document.querySelectorAll('.nd-checkbox').forEach(cb => cb.checked = checked);
  },
  
  updateSelectAllCheckbox() {
    const all = document.querySelectorAll('.nd-checkbox');
    const checked = document.querySelectorAll('.nd-checkbox:checked');
    const selectAllCb = document.getElementById('nd-select-all');
    if (selectAllCb) {
        selectAllCb.checked = all.length > 0 && all.length === checked.length;
    }
  },
  
  async markSelectedRead() {
    const selected = Array.from(document.querySelectorAll('.nd-checkbox:checked')).map(cb => parseInt(cb.value));
    if (selected.length === 0) return utils.showToast('No notifications selected', 'error');
    
    for (let id of selected) {
        try {
            await api.post(`/notifications/${id}/read/`, {});
            const notif = this.notifications.find(n => n.notification_id === id);
            if (notif) notif.is_read = true;
        } catch(e) {}
    }
    this.updateCounters();
    this.render();
    utils.showToast(`Marked ${selected.length} notifications as read`, 'success');
  },
  
  async deleteSelected() {
    const selected = Array.from(document.querySelectorAll('.nd-checkbox:checked')).map(cb => parseInt(cb.value));
    if (selected.length === 0) return utils.showToast('No notifications selected', 'error');
    if(!confirm(`Are you sure you want to delete ${selected.length} notifications?`)) return;
    
    for (let id of selected) {
        try {
            await api.post(`/notifications/${id}/hide/`, {});
            this.notifications = this.notifications.filter(n => n.notification_id !== id);
        } catch(e) {}
    }
    this.updateCounters();
    this.render();
    utils.showToast(`Deleted ${selected.length} notifications`, 'success');
  }
};

// Global Notification Service for Live Notifications
const NotificationService = {
  interval: null,
  
  startPolling() {
    if (this.interval) return;
    this.poll(); // Initial poll
    // Removed setInterval as per user request to stop API spam
  },
  
  stopPolling() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  },
  
  poll() {
    if (!auth.checkAuth()) return;
    
    api.get('/notifications/unread/')
      .then(data => {
        this.updateBadge(data.count);
        this.showNewToasts(data.notifications);
        if (NotificationDrawer.isOpen) {
          NotificationDrawer.fetchNotifications();
        }
      })
      .catch(err => console.error('Notification poll failed', err));
  },
  
  updateBadge(count) {
    const badges = document.querySelectorAll('.notification-badge');
    badges.forEach(badge => {
      if (count > 0) {
        badge.textContent = count > 9 ? '9+' : count;
        badge.classList.remove('hidden');
      } else {
        badge.classList.add('hidden');
      }
    });
  },
  
  showNewToasts(notifications) {
    if (!notifications || !notifications.length) return;
    
    let toastedStr = localStorage.getItem('toasted_notifications') || '[]';
    let toasted = JSON.parse(toastedStr);
    let hasNew = false;
    
    notifications.forEach(notif => {
      if (!toasted.includes(notif.notification_id)) {
        utils.showToast(notif.title + ': ' + notif.description, notif.notification_type || 'info');
        toasted.push(notif.notification_id);
        hasNew = true;
      }
    });
    
    if (hasNew) {
      if (toasted.length > 50) toasted = toasted.slice(toasted.length - 50);
      localStorage.setItem('toasted_notifications', JSON.stringify(toasted));
    }
  }
};

// Start polling on load if authenticated
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('access_token')) {
        NotificationService.startPolling();
    }
});


utils.exportTableToCSV = function(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    let csv = [];
    for (let i = 0; i < table.rows.length; i++) {
        let row = [], cols = table.rows[i].querySelectorAll('td, th');
        
        let limit = cols.length;
        if (i === 0 && cols[limit - 1] && cols[limit - 1].innerText.trim().toLowerCase() === 'actions') {
            limit = cols.length - 1;
        } else if (i > 0 && table.rows[0].querySelectorAll('th').length > 0) {
            const headerCols = table.rows[0].querySelectorAll('th');
            if (headerCols[headerCols.length - 1].innerText.trim().toLowerCase() === 'actions') {
                limit = cols.length - 1;
            }
        }
        
        for (let j = 0; j < limit; j++) {


            let data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/"/g, '""').trim();
            row.push('"' + data + '"');
        }
        csv.push(row.join(','));
    }
    const csvFile = new Blob([csv.join('\n')], {type: 'text/csv'});
    const downloadLink = document.createElement('a');
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
};

utils.showTableSkeleton = function(target, colCount, rowCount = 5) {
    const tbody = (typeof target === 'string') ? document.querySelector(target) : target;
    if (!tbody) return;
    
    let skeletonHtml = '';
    for (let r = 0; r < rowCount; r++) {
        skeletonHtml += `<tr class="animate-pulse border-b border-slate-100">`;
        for (let c = 0; c < colCount; c++) {
            skeletonHtml += `
                <td class="py-4 px-4">
                    <div class="skeleton-bar"></div>
                </td>`;
        }
        skeletonHtml += `</tr>`;
    }
    tbody.innerHTML = skeletonHtml;
};


utils.showViewModal = function(title, dataObj) {
    let modal = document.getElementById('genericViewModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'genericViewModal';
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center hidden modal-overlay';
        modal.innerHTML = `
            <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity opacity-0" id="genericViewModalOverlay" onclick="utils.hideViewModal()"></div>
            <div class="relative bg-white p-8 rounded-2xl shadow-2xl max-w-lg w-full mx-4 transform scale-95 transition-all duration-300 opacity-0 max-h-[90vh] overflow-y-auto" id="genericViewModalContent">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-xl font-bold text-slate-800 font-outfit" id="genericViewModalTitle">Details</h3>
                    <button class="text-slate-400 hover:text-slate-600 transition-colors p-1 hover:bg-slate-100 rounded-lg" onclick="utils.hideViewModal()">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>
                <div id="genericViewModalBody" class="space-y-1 text-sm text-slate-600">
                </div>
                <div class="flex justify-end pt-5 mt-6 border-t border-slate-100">
                    <button class="px-5 py-2.5 rounded-xl font-medium bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors" onclick="utils.hideViewModal()">Close</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
    
    document.getElementById('genericViewModalTitle').innerText = title || 'Record Details';
    
    const body = document.getElementById('genericViewModalBody');
    body.innerHTML = '';
    
    // Ignore internal keys
    const excludeKeys = ['password', 'token', 'refresh'];
    
    for (const [key, value] of Object.entries(dataObj)) {
        if (excludeKeys.includes(key)) continue;
        
        let displayValue = value;
        if (typeof value === 'object' && value !== null) {
            // Flatten nested objects slightly or display cleanly
            if (value.name) displayValue = value.name;
            else if (value.subject_name) displayValue = value.subject_name;
            else displayValue = `<pre class="text-xs bg-slate-50 p-2 rounded mt-1 border border-slate-100">${JSON.stringify(value, null, 2)}</pre>`;
        } else if (value === true) displayValue = 'Yes';
        else if (value === false) displayValue = 'No';
        else if (value === null || value === '') displayValue = '<span class="text-slate-400 italic">Not provided</span>';
        
        body.innerHTML += `
            <div class="grid grid-cols-3 gap-2 py-2.5 border-b border-slate-50 last:border-0">
                <div class="font-semibold text-slate-800 capitalize">${key.replace(/_/g, ' ')}</div>
                <div class="col-span-2 text-slate-600 break-words">${displayValue}</div>
            </div>
        `;
    }
    
    modal.classList.remove('hidden');
    modal.classList.add('active');
    // small delay to allow display:block to apply before animating opacity
    setTimeout(() => {
        const overlay = document.getElementById('genericViewModalOverlay');
        const content = document.getElementById('genericViewModalContent');
        if (overlay) overlay.classList.remove('opacity-0');
        if (content) content.classList.remove('opacity-0', 'scale-95');
    }, 10);
};

utils.hideViewModal = function() {
    const overlay = document.getElementById('genericViewModalOverlay');
    const content = document.getElementById('genericViewModalContent');
    const modal = document.getElementById('genericViewModal');
    if(overlay) overlay.classList.add('opacity-0');
    if(content) content.classList.add('opacity-0', 'scale-95');
    if(modal) modal.classList.remove('active');
    setTimeout(() => {
        if(modal) modal.classList.add('hidden');
    }, 300);
};


document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('aside');
    let overlay = null;
    if (sidebar) {
        overlay = document.getElementById(sidebar.id + 'Overlay');
    }
    
    if (sidebar && toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            if (window.innerWidth < 1024) {
                sidebar.classList.toggle('-translate-x-full');
                if (!sidebar.classList.contains('-translate-x-full')) sidebar.style.transform = 'translateX(0)';
                else sidebar.style.transform = '';
                if (overlay) overlay.classList.toggle('hidden');
            } else {
                sidebar.classList.toggle('collapsed-sidebar');
            }
        });
    }

    const closeBtns = document.querySelectorAll('.close-sidebar-btn');
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (sidebar) {
                sidebar.classList.add('-translate-x-full');
                sidebar.style.transform = '';
            }
            if (overlay) {
                overlay.classList.add('hidden');
            }
        });
    });

    if (overlay) {
        overlay.addEventListener('click', () => {
            if (sidebar) {
                sidebar.classList.add('-translate-x-full');
                sidebar.style.transform = '';
            }
            overlay.classList.add('hidden');
        });
    }
});



// Global action menu click handler
document.addEventListener('click', (e) => {
    // Check if clicked element is the three dots button or inside it
    let btn = e.target.closest('button');
    const isActionBtn = btn && btn.querySelector('.bi-three-dots-vertical');
    
    // Close all action dropdowns except the one we just clicked
    document.querySelectorAll('.action-menu-dropdown').forEach(menu => {
        if (!isActionBtn || menu.previousElementSibling !== btn) {
            menu.classList.remove('opacity-100', 'visible', 'scale-100');
            menu.classList.add('opacity-0', 'invisible', 'scale-95');
            if (menu.parentElement) menu.parentElement.classList.remove('z-50');
        }
    });

    // If an action button was clicked, toggle its menu
    if (isActionBtn) {
        const menu = btn.nextElementSibling;
        if (menu && menu.classList.contains('action-menu-dropdown')) {
            if (menu.classList.contains('opacity-0')) {
                // Open it
                menu.classList.remove('opacity-0', 'invisible', 'scale-95');
                menu.classList.add('opacity-100', 'visible', 'scale-100');
                if (menu.parentElement) menu.parentElement.classList.add('z-50');
            } else {
                // Close it
                menu.classList.add('opacity-0', 'invisible', 'scale-95');
                menu.classList.remove('opacity-100', 'visible', 'scale-100');
                if (menu.parentElement) menu.parentElement.classList.remove('z-50');
            }
        }
    }
});



// Global bell icon click listener
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#bellNotify').forEach(btn => {
        btn.addEventListener('click', () => {
            if (typeof NotificationDrawer !== 'undefined') {
                NotificationDrawer.toggle();
            }
        });
    });
});


// Global popover filter click handler
document.addEventListener('click', (e) => {
    if (e.target.closest('.filter-popover-content')) return;
    let btn = e.target.closest('.filter-popover-trigger');
    document.querySelectorAll('.filter-popover-content').forEach(menu => {
        if (!btn || menu.previousElementSibling !== btn) {
            menu.classList.add('hidden');
            menu.parentElement.classList.remove('z-50');
        }
    });
    if (btn) {
        const menu = btn.nextElementSibling;
        if (menu && menu.classList.contains('filter-popover-content')) {
            menu.classList.toggle('hidden');
            if (!menu.classList.contains('hidden')) {
                menu.parentElement.classList.add('z-50');
                
                // Escape overflow hidden container
                menu.style.position = 'fixed';
                const rect = btn.getBoundingClientRect();
                
                // Determine if it should drop up or down
                if (rect.bottom + 250 > window.innerHeight) {
                    menu.style.top = 'auto';
                    menu.style.bottom = (window.innerHeight - rect.top + 4) + 'px';
                } else {
                    menu.style.bottom = 'auto';
                    menu.style.top = (rect.bottom + 4) + 'px';
                }
                menu.style.left = rect.left + 'px';
                menu.style.marginTop = '0';
                
                const input = menu.querySelector('input, select');
                if (input) setTimeout(() => input.focus(), 10);
            } else {
                menu.parentElement.classList.remove('z-50');
            }
        }
    }
});



// Convert standard selects inside popovers to Ant Design Table Filters
function createAntFilterMenu(selectEl) {
    if (selectEl.dataset.antified === 'true') return;
    selectEl.dataset.antified = 'true';
    selectEl.style.display = 'none'; // hide original select
    
    const popoverContent = selectEl.closest('.filter-popover-content');
    if (popoverContent) {
        popoverContent.classList.remove('p-2');
        popoverContent.classList.add('p-0', 'overflow-hidden', 'shadow-lg', 'rounded-lg', 'border', 'border-slate-200');
    }

    const container = document.createElement('div');
    container.className = 'ant-table-filter-dropdown bg-white flex flex-col min-w-[200px]';
    
    const ul = document.createElement('ul');
    ul.className = 'ant-dropdown-menu py-2 px-3 m-0 list-none text-[14px] text-slate-700 max-h-[250px] overflow-y-auto space-y-2';
    
    const renderOptions = () => {
        ul.innerHTML = '';
        Array.from(selectEl.options).forEach(opt => {
            if(!opt.value && opt.text.toLowerCase().includes('all')) return; // Skip "All" if we use reset
            const li = document.createElement('li');
            li.className = 'flex items-center gap-3 py-1 cursor-pointer';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'w-[15px] h-[15px] cursor-pointer rounded border-slate-300 accent-[#2563eb]';
            checkbox.value = opt.value;
            checkbox.checked = selectEl.value === opt.value;
            
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    ul.querySelectorAll('input[type="checkbox"]').forEach(cb => {
                        if (cb !== checkbox) cb.checked = false;
                    });
                }
            });
            
            const span = document.createElement('span');
            span.textContent = opt.text;
            span.className = 'text-slate-700 font-normal select-none';
            
            li.appendChild(checkbox);
            li.appendChild(span);
            
            li.addEventListener('click', (e) => {
                if (e.target !== checkbox) {
                    checkbox.checked = !checkbox.checked;
                    checkbox.dispatchEvent(new Event('change'));
                }
            });
            ul.appendChild(li);
        });
    };
    
    renderOptions();
    
    const btnContainer = document.createElement('div');
    btnContainer.className = 'flex justify-between items-center px-4 py-2.5 border-t border-blue-100/60 bg-white';
    
    const resetBtn = document.createElement('button');
    resetBtn.className = 'text-[13px] text-[#a0aec0] hover:text-slate-600 bg-transparent border-none cursor-pointer p-0 m-0';
    resetBtn.textContent = 'Reset';
    resetBtn.onclick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        ul.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
        selectEl.value = '';
        selectEl.dispatchEvent(new Event('change'));
        if (popoverContent) {
            popoverContent.classList.add('hidden');
            if (popoverContent.parentElement) popoverContent.parentElement.classList.remove('z-50');
        }
    };
    
    const okBtn = document.createElement('button');
    okBtn.className = 'text-[13px] font-medium bg-[#2563eb] text-white rounded px-4 py-1.5 hover:bg-blue-700 transition-colors border-none cursor-pointer';
    okBtn.textContent = 'OK';
    okBtn.onclick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        const checked = ul.querySelector('input[type="checkbox"]:checked');
        selectEl.value = checked ? checked.value : '';
        selectEl.dispatchEvent(new Event('change'));
        if (popoverContent) {
            popoverContent.classList.add('hidden');
            if (popoverContent.parentElement) popoverContent.parentElement.classList.remove('z-50');
        }
    };
    
    btnContainer.appendChild(resetBtn);
    btnContainer.appendChild(okBtn);
    
    container.appendChild(ul);
    container.appendChild(btnContainer);
    
    selectEl.parentNode.insertBefore(container, selectEl.nextSibling);
    
    const observer = new MutationObserver(() => renderOptions());
    observer.observe(selectEl, { childList: true });
}

// Intercept popover open to initialize Ant filters
const originalPopoverHandler = document.addEventListener;
document.addEventListener('click', (e) => {
    let btn = e.target.closest('.filter-popover-trigger');
    if (btn) {
        const menu = btn.nextElementSibling;
        if (menu && menu.classList.contains('filter-popover-content')) {
            const select = menu.querySelector('select');
            if (select) {
                createAntFilterMenu(select);
            }
        }
    }
});

// Escape overflow hidden for Action menus
document.addEventListener('mouseover', (e) => {
    const menuContainer = e.target.closest('.group\\/menu');
    if (menuContainer) {
        const dropdown = menuContainer.querySelector('div[class*="absolute"]');
        if (dropdown && dropdown.style.position !== 'fixed') {
            dropdown.style.position = 'fixed';
            const rect = menuContainer.getBoundingClientRect();
            // Check if it goes off bottom of screen
            if (rect.bottom + 150 > window.innerHeight) {
                dropdown.style.top = 'auto';
                dropdown.style.bottom = (window.innerHeight - rect.top + 4) + 'px';
            } else {
                dropdown.style.bottom = 'auto';
                dropdown.style.top = (rect.bottom + 4) + 'px';
            }
            dropdown.style.left = (rect.right - 144) + 'px'; 
            dropdown.style.marginTop = '0';
        }
    }
});

// Update position if scrolling happens while hovering
document.addEventListener('wheel', (e) => {
    document.querySelectorAll('.group\\/menu div[class*="absolute"]').forEach(dropdown => {
        if (dropdown.style.position === 'fixed' && window.getComputedStyle(dropdown).opacity !== '0') {
            const menuContainer = dropdown.closest('.group\\/menu');
            if(menuContainer){
                const rect = menuContainer.getBoundingClientRect();
                dropdown.style.left = (rect.right - 144) + 'px';
                if (rect.bottom + 150 > window.innerHeight) {
                    dropdown.style.top = 'auto';
                    dropdown.style.bottom = (window.innerHeight - rect.top + 4) + 'px';
                } else {
                    dropdown.style.bottom = 'auto';
                    dropdown.style.top = (rect.bottom + 4) + 'px';
                }
            }
        }
    });
}, {passive: true});


// Update position if scrolling happens while filter popover is open
document.addEventListener('wheel', (e) => {
    document.querySelectorAll('.filter-popover-content').forEach(menu => {
        if (!menu.classList.contains('hidden') && menu.style.position === 'fixed') {
            const btn = menu.previousElementSibling;
            if (btn) {
                const rect = btn.getBoundingClientRect();
                menu.style.left = rect.left + 'px';
                if (rect.bottom + 250 > window.innerHeight) {
                    menu.style.top = 'auto';
                    menu.style.bottom = (window.innerHeight - rect.top + 4) + 'px';
                } else {
                    menu.style.bottom = 'auto';
                    menu.style.top = (rect.bottom + 4) + 'px';
                }
            }
        }
    });
}, {passive: true});
