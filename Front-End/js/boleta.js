document.addEventListener('DOMContentLoaded', function () {
    const boleta = JSON.parse(localStorage.getItem('boleta')) || null;
    const boletaInfoContainer = document.getElementById('boleta-info');

    function mostrarBoleta() {
        if (boleta) {
            const productosHTML = boleta.productos.map(producto => `
                <li>${producto.title} - ${producto.quantity} x $${producto.price} = $${producto.price * producto.quantity}</li>
            `).join('');

            const reservaHTML = boleta.reserva ? `
                <h4>Detalles de la Reserva</h4>
                <p><strong>Nombre:</strong> ${boleta.reserva.nombre}</p>
                <p><strong>Personas:</strong> ${boleta.reserva.personas}</p>
                <p><strong>Fecha:</strong> ${boleta.reserva.fecha}</p>
                <p><strong>Hora:</strong> ${boleta.reserva.hora}</p>
            ` : '<p>No se realizó ninguna reserva.</p>';

            boletaInfoContainer.innerHTML = `
                <h3>Información del Cliente</h3>
                <p><strong>Nombre:</strong> ${boleta.usuario}</p>
                <p><strong>Mail:</strong> ${boleta.mail}</p>
                <h3>Productos Comprados</h3>
                <ul>${productosHTML}</ul>
                <h3>Total a Pagar</h3>
                <p><strong>Total:</strong> $${boleta.total}</p>
                <h3>Método de Pago</h3>
                <p>${boleta.metodo_pago}</p>
                ${reservaHTML}
            `;
        } else {
            boletaInfoContainer.innerHTML = '<p>No se encontró información de la boleta.</p>';
        }
    }

    mostrarBoleta();
});