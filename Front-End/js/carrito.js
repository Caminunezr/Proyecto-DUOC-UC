document.addEventListener('DOMContentLoaded', function () {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    actualizarCarritoUI();

    function actualizarCarritoUI() {
        const detallesCarrito = document.getElementById('cart-items');
        detallesCarrito.innerHTML = '';

        let totalPrecio = 0;

        carrito.forEach((producto, index) => {
            totalPrecio += producto.price * producto.quantity;

            const productElement = document.createElement('div');
            productElement.classList.add('cart-item');
            productElement.innerHTML = `
                <img src="${producto.image}" alt="${producto.title}">
                <div class="cart-item-details">
                    <div class="cart-item-title">${producto.title}</div>
                    <div class="cart-item-quantity">
                        <button class="disminuir-cantidad" data-index="${index}">-</button>
                        <span>${producto.quantity}</span>
                        <button class="aumentar-cantidad" data-index="${index}">+</button>
                    </div>
                    <div class="cart-item-price">$${producto.price * producto.quantity}</div>
                </div>
                <button class="eliminar-producto" data-index="${index}">Eliminar</button>
            `;
            detallesCarrito.appendChild(productElement);
        });

        document.getElementById('total-price').textContent = `CLP ${totalPrecio.toFixed(0)}`;
    }

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('aumentar-cantidad')) {
            const index = parseInt(event.target.getAttribute('data-index'));
            carrito[index].quantity++;
            localStorage.setItem('carrito', JSON.stringify(carrito));
            actualizarCarritoUI();
        }

        if (event.target.classList.contains('disminuir-cantidad')) {
            const index = parseInt(event.target.getAttribute('data-index'));
            if (carrito[index].quantity > 1) {
                carrito[index].quantity--;
            } else {
                carrito.splice(index, 1);
            }
            localStorage.setItem('carrito', JSON.stringify(carrito));
            actualizarCarritoUI();
        }

        if (event.target.classList.contains('eliminar-producto')) {
            const index = parseInt(event.target.getAttribute('data-index'));
            carrito.splice(index, 1);
            localStorage.setItem('carrito', JSON.stringify(carrito));
            actualizarCarritoUI();
        }
    });

    document.getElementById('checkout-btn').addEventListener('click', function () {
        window.location.href = 'pago.html';  // Asegúrate de que esta sea la ruta correcta
    });
});