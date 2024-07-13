document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const user = {
        username: email, // Usar el correo electrónico como nombre de usuario
        password: password
    };

    // Enviar solicitud POST al backend
    fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login fallido');
        }
        return response.json();
    })
    .then(data => {
        localStorage.setItem('accessToken', data.access); // Guardar el token de acceso en localStorage
        alert('Login exitoso');
        window.location.href = 'index.html'; // Redirigir a la página de inicio
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al iniciar sesión');
    });
});

document.getElementById('togglePassword').addEventListener('click', function() {
    const password = document.getElementById('password');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});