document.getElementById('resetForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const apiKey = '87ee40fd4dbf46a2bccd5ff071680a24';

    fetch(`https://api.zerobounce.net/v2/validate?api_key=${apiKey}&email=${email}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'valid') {
                alert(`Correo electrónico válido. Se enviarán las instrucciones de restablecimiento a ${email}.`);
                // Aquí puedes agregar el código para enviar el correo de restablecimiento
            } else {
                alert(`Correo electrónico no válido: ${data.sub_status}`);
            }
        })
        .catch(error => {
            alert('Error al verificar el correo electrónico. Inténtelo nuevamente.');
            console.error(error);
        });
});
