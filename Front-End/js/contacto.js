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
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                document.getElementById('logout-btn').classList.remove('d-none');
                document.getElementById('login-btn').classList.add('d-none');
                document.getElementById('register-btn').classList.add('d-none');
                document.getElementById('user-greeting').classList.remove('d-none');
                document.getElementById('user-name').textContent = data.first_name;

                // Ocultar campos de nombre y correo si el usuario está autenticado
                document.getElementById('name-field').classList.add('d-none');
                document.getElementById('email-field').classList.add('d-none');
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

    document.getElementById('contact-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        const data = { message };

        if (!token) {
            data.name = name;
            data.email = email;
        }

        fetch('http://127.0.0.1:8000/api/mensajes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                alert('Mensaje enviado exitosamente');
                document.getElementById('contact-form').reset();
            } else {
                throw new Error('Error al enviar el mensaje');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al enviar el mensaje');
        });
    });
});
