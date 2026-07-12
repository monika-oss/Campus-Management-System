const API_BASE = 'https://campus-management-system-production-7bbb.up.railway.app/api';

const api = {
  async request(method, endpoint, data = null) {
    const token = localStorage.getItem('access_token');
    const config = {
      method,
      headers: {
        'Content-Type': 'application/json',
      }
    };

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    if (data) {
      config.body = JSON.stringify(data);
    }
    
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, config);
      
      if (response.status === 401 && endpoint !== '/auth/login/' && endpoint !== '/auth/refresh/') {
        // Try token refresh
        const refreshed = await api.refreshToken();
        if (refreshed) {
            return api.request(method, endpoint, data);
        } else {
            // Refresh failed, logout and clear credentials
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_data');
            const depth = window.location.pathname.split('/').length - 2;
            window.location.href = depth > 0 ? '../'.repeat(depth) + 'index.html' : 'index.html';
            return null;
        }
      }
      
      const responseData = await response.json().catch(() => ({}));
      
      if (!response.ok) {
        throw { status: response.status, data: responseData };
      }
      
      return responseData;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },
  
  get: (endpoint) => api.request('GET', endpoint),
  post: (endpoint, data) => api.request('POST', endpoint, data),
  put: (endpoint, data) => api.request('PUT', endpoint, data),
  patch: (endpoint, data) => api.request('PATCH', endpoint, data),
  delete: (endpoint) => api.request('DELETE', endpoint),
  
  async refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return false;
    
    try {
      const res = await fetch(`${API_BASE}/auth/refresh/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({refresh})
      });
      
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('access_token', data.access);
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
};
