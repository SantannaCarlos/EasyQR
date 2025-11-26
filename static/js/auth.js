const API_BASE_URL = 'http://localhost:8000/api/v1';

const USERS = {
    'admin': { password: 'admin123', name: 'Administrador' },
    'user': { password: 'user123', name: 'Usuário' }
};

function checkAuth() {
    const user = sessionStorage.getItem('user');
    const currentPage = window.location.pathname;
    const publicPages = ['/', '/login', '/login.html'];

    if (!user && !publicPages.includes(currentPage)) {
        window.location.href = '/login';
        return false;
    }

    if (user && publicPages.includes(currentPage)) {
        window.location.href = '/dashboard';
        return false;
    }

    return true;
}

function login(username, password) {
    const user = USERS[username];

    if (user && user.password === password) {
        const userData = {
            username: username,
            name: user.name,
            loginTime: new Date().toISOString()
        };
        sessionStorage.setItem('user', JSON.stringify(userData));
        return { success: true, user: userData };
    }

    return { success: false, message: 'Usuário ou senha inválidos' };
}

function logout() {
    sessionStorage.removeItem('user');
    window.location.href = '/login';
}

function getCurrentUser() {
    const userData = sessionStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
}

function updateUserInfo() {
    const user = getCurrentUser();
    const userInfoElement = document.getElementById('userInfo');

    if (user && userInfoElement) {
        userInfoElement.textContent = `Olá, ${user.name}`;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    updateUserInfo();
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('loginError');

            const result = login(username, password);

            if (result.success) {
                window.location.href = '/dashboard';
            } else {
                errorDiv.textContent = result.message;
                errorDiv.style.display = 'block';
            }
        });
    }
});

// Funções auxiliares para chamadas à API
async function apiRequest(endpoint, options = {}) {
    const startTime = performance.now();

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                ...options.headers,
            }
        });

        const endTime = performance.now();
        const responseTime = endTime - startTime;

        console.log(`API Request: ${endpoint} - ${responseTime.toFixed(2)}ms`);

        return {
            response,
            responseTime,
            ok: response.ok
        };
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
