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

    const birthDate = `2024-${month.padStart(2, '0')}-${day.padStart(2, '0')}`; // Formatear la fecha de nacimiento

    // Crear datos del usuario
    const user = {
        username: email, // Usar el correo electrónico como nombre de usuario
        email,
        first_name: firstName,
        last_name: lastName,
        birth_date: birthDate,
        password
    };

    // Enviar solicitud POST al backend
    fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Registro fallido');
            });
        }
        return response.json();
    })
    .then(data => {
        alert('Registro exitoso');
        // Redirigir a la página de inicio de sesión
        window.location.href = 'login.html';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al registrar el usuario');
    });
});

document.getElementById('togglePassword').addEventListener('click', function() {
    const password = document.getElementById('password');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});