document.getElementById('resetForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;

    // Simular el envío de instrucciones de restablecimiento de contraseña
    alert(`Se han enviado instrucciones para restablecer la contraseña a ${email}`);
});