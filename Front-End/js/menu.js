document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('accessToken');

    if (token) {
        fetch('http://127.0.0.1:8000/api/user-info/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Unauthorized');
            }
            return response.json();
        })
        .then(data => {
            if (data.username) {
                document.getElementById('user-name').textContent = data.username;
                document.getElementById('user-greeting').classList.remove('d-none');
                document.getElementById('logout-btn').classList.remove('d-none');
                document.getElementById('cart-icon-container').classList.remove('d-none');
            } else {
                document.getElementById('login-btn').classList.remove('d-none');
                document.getElementById('register-btn').classList.remove('d-none');
            }
        })
        .catch(error => {
            console.error('Error fetching user info:', error);
            document.getElementById('login-btn').classList.remove('d-none');
            document.getElementById('register-btn').classList.remove('d-none');
        });
    } else {
        document.getElementById('login-btn').classList.remove('d-none');
        document.getElementById('register-btn').classList.remove('d-none');
    }

    document.getElementById('logout-btn').addEventListener('click', function() {
        localStorage.removeItem('accessToken');
        window.location.href = 'login.html';
    });

    // Añadir evento de clic al icono del carrito
    document.getElementById('cart-icon-container').addEventListener('click', function() {
        window.location.href = 'carrito.html';
    });

    // Manejar el evento de agregar al carrito
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const product = {
                title: this.getAttribute('data-name'),
                price: parseInt(this.getAttribute('data-price')),
                image: this.getAttribute('data-image'),
                quantity: 1
            };

            let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
            const existingProductIndex = carrito.findIndex(item => item.title === product.title);

            if (existingProductIndex !== -1) {
                carrito[existingProductIndex].quantity++;
            } else {
                carrito.push(product);
            }

            localStorage.setItem('carrito', JSON.stringify(carrito));
            actualizarCarritoUI();
        });
    });

    function actualizarCarritoUI() {
        let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
        const cartCount = document.getElementById('cart-count');
        cartCount.textContent = carrito.length;
        cartCount.style.display = carrito.length > 0 ? 'inline' : 'none';
    }

    actualizarCarritoUI();
});