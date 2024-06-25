$(document).ready(function() {
    
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    actualizarCarritoUI();

    $('.agregar-carrito').click(function() {
        const item = $(this).closest('.postre');
        const itemTitulo = item.find('h2').text();
        const itemPrecio = parseFloat(item.find('.precio').text().replace('$', ''));
        const itemImagen = item.find('.plato img').attr('src');  // Obtener la URL de la imagen
    
        // Verificar si el producto ya existe en el carrito
        const productoEnCarrito = carrito.find(producto => producto.titulo === itemTitulo);
        if (productoEnCarrito) {
            productoEnCarrito.cantidad++;  // Solo incrementa la cantidad
        } else {
            // Si el producto no está en el carrito, añadirlo
            carrito.push({ titulo: itemTitulo, precio: itemPrecio, cantidad: 1, imagen: itemImagen });
        }
        
        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarCarritoUI();
    });
    
    
    function actualizarCarritoUI() {
        const detallesCarrito = $('#detalles-carrito');
        detallesCarrito.empty();
        
        let totalPrecio = 0;
        
        carrito.forEach((producto, index) => {
            totalPrecio += producto.precio * producto.cantidad;
        
            detallesCarrito.append(`
                <div>
                    <img src="${producto.imagen}" alt="${producto.titulo}" style="width: 50px; height: auto; float: left; margin-right: 10px;">
                    ${producto.titulo} - 
                    <button class="disminuir-cantidad" data-index="${index}">-</button> 
                    ${producto.cantidad} 
                    <button class="aumentar-cantidad" data-index="${index}">+</button> 
                     x $${producto.precio}  =  $${producto.precio * producto.cantidad}
                    <button class="eliminar-producto" data-index="${index}">Eliminar</button>
                </div>`);
        });
    
        // Solo actualiza el total de precio en el lugar específico
        $('#precio-total').text(totalPrecio.toFixed(0));
    }
    
    
    
    // Funcionalidad para mostrar/ocultar la barra lateral del carrito
    $('#mostrar-carrito').click(function() {
    $('#carrito-lateral').toggle();
    });

    $('#vaciar-carrito').click(function() {
    carrito = [];
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarritoUI();
    });

   // Manejar el evento clic para aumentar la cantidad
$(document).on('click', '.aumentar-cantidad', function() {
    const index = parseInt($(this).data('index')); // Asegúrate de convertir el índice a número
    carrito[index].cantidad++;
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarritoUI();
});

// Manejar el evento clic para disminuir la cantidad
$(document).on('click', '.disminuir-cantidad', function() {
    const index = parseInt($(this).data('index')); // Asegúrate de convertir el índice a número
    if (carrito[index].cantidad > 1) {
        carrito[index].cantidad--;
    } else {
        carrito.splice(index, 1); // Eliminar el producto si la cantidad es 0
    }
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarritoUI();
});

    // Manejar el evento clic para eliminar un producto
    $(document).on('click', '.eliminar-producto', function() {
        const index = $(this).data('index');
        carrito.splice(index, 1);
        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarCarritoUI();
    });

    $(document).on('click', '#pagar-carrito', function() {
        window.location.href = 'Carrito.html';
    });

    // Manejar el evento clic para el botón "Pagar"
$(document).on('click', '#btn-pagar', function() {
    window.location.href = 'index.html';  // Cambia aquí a la página que deseas que redirija
});

});
