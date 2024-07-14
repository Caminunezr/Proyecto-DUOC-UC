document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('accessToken');
    
    if (token) {
        fetch('http://127.0.0.1:8000/api/user-info/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Unauthorized');
            }
            return response.json();
        })
        .then(data => {
            if (data.username) {
                document.getElementById('user-name').textContent = data.username;
                document.getElementById('user-greeting').classList.remove('d-none');
                document.getElementById('logout-btn').classList.remove('d-none');
            } else {
                document.getElementById('login-btn').classList.remove('d-none');
                document.getElementById('register-btn').classList.remove('d-none');
            }
        })
        .catch(error => {
            console.error('Error fetching user info:', error);
            document.getElementById('login-btn').classList.remove('d-none');
            document.getElementById('register-btn').classList.remove('d-none');
        });
    } else {
        document.getElementById('login-btn').classList.remove('d-none');
        document.getElementById('register-btn').classList.remove('d-none');
    }

    document.getElementById('logout-btn').addEventListener('click', function() {
        localStorage.removeItem('accessToken');
        window.location.href = 'login.html';
    });
});