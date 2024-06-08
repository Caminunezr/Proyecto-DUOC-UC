document.addEventListener('DOMContentLoaded', function() {
    const daySelect = document.getElementById('day');
    for (let i = 1; i <= 31; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        daySelect.appendChild(option);
    }
});

document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const day = document.getElementById('day').value;
    const month = document.getElementById('month').value;

    // Validaciones de ejemplo
    if (password.length < 6) {
        alert('Password must be at least 6 characters long');
        return;
    }

    // Guardar datos en localStorage
    const user = {
        firstName,
        lastName,
        email,
        password,
        day,
        month
    };
    localStorage.setItem('user', JSON.stringify(user));

    alert('Registration successful');
    // Redirigir a la página de inicio de sesión
    window.location.href = 'login.html';
});

document.getElementById('togglePassword').addEventListener('click', function() {
    const password = document.getElementById('password');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});