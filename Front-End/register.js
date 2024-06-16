document.addEventListener('DOMContentLoaded', function() {
    const daySelect = document.getElementById('day');
    const monthSelect = document.getElementById('month');

    function populateDays(month) {
        daySelect.innerHTML = '<option value="" disabled selected>Día</option>'; // Clear previous options
        const daysInMonth = new Date(2024, month, 0).getDate();
        for (let i = 1; i <= daysInMonth; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            daySelect.appendChild(option);
        }
    }

    monthSelect.addEventListener('change', function() {
        const selectedMonth = parseInt(monthSelect.value);
        if (!isNaN(selectedMonth)) {
            populateDays(selectedMonth);
        }
    });

    // Initialize days for the default selected month if any
    if (monthSelect.value) {
        populateDays(parseInt(monthSelect.value));
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
        alert('La contraseña debe tener al menos 6 caracteres');
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

    alert('Registro exitoso');
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