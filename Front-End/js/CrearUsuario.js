document.addEventListener("DOMContentLoaded", function() {
    // Obtener el formulario
    const form = document.getElementById("userForm");

    // Agregar evento de envío al formulario
    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevenir el envío del formulario por defecto

        // Obtener datos del formulario
        const nombre = document.getElementById("nombre").value;
        const apellidos = document.getElementById("apellidos").value;
        const rut = document.getElementById("rut").value;
        const edad = document.getElementById("edad").value;
        const carrera = document.getElementById("carrera").value;
        const email = document.getElementById("email").value;
        const duoc = document.getElementById("duoc").value;
        const password = document.getElementById("password").value;
        const confirm_password = document.getElementById("confirm_password").value;

        // Verificar si el usuario ya existe en el localStorage
        if (localStorage.getItem(email)) {
            alert("Este usuario ya existe.");
            return; // Detener la ejecución si el usuario ya existe
        }

        // Verificar si las contraseñas coinciden
        if (password !== confirm_password) {
            alert("Las contraseñas no coinciden.");
            return; // Detener la ejecución si las contraseñas no coinciden
        }

        // Crear objeto usuario
        const usuario = {
            nombre: nombre,
            apellidos: apellidos,
            rut: rut,
            edad: edad,
            carrera: carrera,
            email: email,
            duoc: duoc,
            password: password
        };
        // Enviar solicitud POST al backend
    fetch('http://127.0.0.1:8000/api/CrearUsuario/', {
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
        // Guardar usuario en localStorage
        localStorage.setItem(email, JSON.stringify(usuario));

        // Redirigir a otra página
        window.location.href = "UsuarioListo.html";
    });