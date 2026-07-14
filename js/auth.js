// Helper: get root-relative path to login page
function getLoginPath() {
  const depth = window.location.pathname.split('/').length - 2;
  return depth > 0 ? '../'.repeat(depth) + 'index.html' : 'index.html';
}

const auth = {
  checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
      window.location.href = getLoginPath();
      return false;
    }
    return true;
  },

  getUser() {
    const userStr = localStorage.getItem('user_data');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch (e) {
        return null;
      }
    }
    return null;
  },

  hasRole(role) {
    const user = this.getUser();
    return user && user.role === role;
  },

  hasDesignation(designation) {
    const user = this.getUser();
    return user && user.role === 'faculty' && user.designation === designation;
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
    window.location.href = getLoginPath();
  },

  login(email, password) {
    const cleanEmail = (email || '').trim();
    const cleanPassword = (password || '').trim();
    return api.post('/auth/login/', { email: cleanEmail, password: cleanPassword })
      .then(data => {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user_data', JSON.stringify(data.user));
        return data.user;
      });
  }
};


// Auto-update profile name in navbar
document.addEventListener('DOMContentLoaded', () => {
    const user = auth.getUser();
    if (user && document.getElementById('userName')) {
        const name = user.name || (user.email ? user.email.split('@')[0] : 'Admin');
        document.getElementById('userName').innerText = name;
        document.getElementById('userAvatar').innerText = name.charAt(0).toUpperCase();
    }
});
