document.addEventListener('DOMContentLoaded', function () {
    fetchBoletas();
});

function fetchBoletas() {
    fetch('http://127.0.0.1:8000/api/boletas/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token YOUR_API_TOKEN'  // Reemplaza YOUR_API_TOKEN con el token de autenticación
        }
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('boletas-table-body');
        tableBody.innerHTML = '';
        data.forEach(boleta => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${boleta.id}</td>
                <td>${boleta.usuario}</td>
                <td>${boleta.venta.producto.nombre}</td>
                <td>${boleta.venta.cantidad}</td>
                <td>${boleta.venta.total_venta}</td>
                <td>${new Date(boleta.fecha_hora).toLocaleString()}</td>
                <td>${boleta.metodo_pago}</td>
                <td>${boleta.reserva ? `Reserva en mesa ${boleta.reserva.mesa.numero}` : 'Sin reserva'}</td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error fetching boletas:', error));
}