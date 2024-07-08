document.addEventListener('DOMContentLoaded', function () {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const reservation = JSON.parse(localStorage.getItem('reservation')) || null;
    const user = JSON.parse(localStorage.getItem('user')) || null;
    const cartItemsContainer = document.getElementById('cart-items');
    const totalPriceContainer = document.getElementById('total-price');
    const userNameContainer = document.getElementById('user-name');
    const reserveInfoContainer = document.getElementById('reservation-info');
    const noReserveInfoContainer = document.getElementById('no-reservation-info');
    const reserveNameContainer = document.getElementById('reserve-name');
    const reserveActivitiesContainer = document.getElementById('reserve-activities');
    const reserveDateContainer = document.getElementById('reserve-date');
    const reserveTimeContainer = document.getElementById('reserve-time');

    function actualizarCarritoUI() {
        let totalPrice = 0;

        carrito.forEach((product) => {
            totalPrice += product.price * product.quantity;
        });

        totalPriceContainer.textContent = totalPrice.toFixed(2);
    }

    function mostrarUsuario() {
        if (user) {
            userNameContainer.textContent = user.username;
        }
    }

    function mostrarReserva() {
        if (reservation) {
            reserveNameContainer.textContent = reservation.name;
            reserveActivitiesContainer.textContent = reservation.activities;
            reserveDateContainer.textContent = reservation.date;
            reserveTimeContainer.textContent = reservation.time;
            reserveInfoContainer.classList.remove('d-none');
        } else {
            noReserveInfoContainer.classList.remove('d-none');
        }
    }

    actualizarCarritoUI();
    mostrarUsuario();
    mostrarReserva();

    document.getElementById('pay-btn').addEventListener('click', function () {
        const paymentMethod = document.querySelector('input[name="payment-method"]:checked').value;

        const boleta = {
            usuario: user.username,
            mail: user.email,
            productos: carrito,
            total: parseFloat(totalPriceContainer.textContent),
            metodo_pago: paymentMethod,
            reserva: reservation ? {
                nombre: reservation.name,
                personas: reservation.activities,
                fecha: reservation.date,
                hora: reservation.time
            } : null
        };

        localStorage.setItem('boleta', JSON.stringify(boleta));
        window.location.href = 'boleta.html';
    });
});