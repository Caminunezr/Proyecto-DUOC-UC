document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('accessToken');
    let userLoggedIn = false;

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
                    document.getElementById('login-btn').classList.add('d-none');
                    document.getElementById('register-btn').classList.add('d-none');
                    document.getElementById('name-group').classList.add('d-none');
                    userLoggedIn = true;
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

    document.getElementById('logout-btn').addEventListener('click', function () {
        localStorage.removeItem('accessToken');
        window.location.href = 'login.html';
    });

    $('#date').datetimepicker({
        timepicker: false,
        format: 'Y-m-d',
        onGenerate: function (ct) {
            $(this).find('.xdsoft_date.xdsoft_weekend')
                .addClass('xdsoft_disabled');
        },
        beforeShowDay: function (date) {
            // Disable Sundays
            var day = date.getDay();
            return [(day != 0), ''];
        }
    });

    $('#time').datetimepicker({
        datepicker: false,
        format: 'H:i',
        allowTimes: [
            '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
            '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
            '14:00', '14:30', '15:00', '15:30', '16:00', '16:30',
            '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
            '20:00'
        ]
    });

    $('#reservation-form').validate({
        rules: {
            name: {
                required: !userLoggedIn,
                minlength: 2
            },
            activities: {
                required: true
            },
            date: {
                required: true,
                date: true
            },
            time: {
                required: true,
                time: true
            }
        },
        messages: {
            name: {
                required: "Por favor ingresa tu nombre",
                minlength: "Tu nombre debe tener al menos 2 caracteres"
            },
            activities: {
                required: "Por favor selecciona el número de personas"
            },
            date: {
                required: "Por favor selecciona una fecha",
                date: "Por favor ingresa una fecha válida"
            },
            time: {
                required: "Por favor selecciona una hora",
                time: "Por favor ingresa una hora válida"
            }
        },
        submitHandler: function (form) {
            let name = $('#name').val();
            let activities = $('#activities').val();
            let date = $('#date').val();
            let time = $('#time').val();

            if (userLoggedIn) {
                fetch('http://127.0.0.1:8000/api/user-info/', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        name = data.username;
                        guardarReserva(name, activities, date, time);
                    })
                    .catch(error => {
                        console.error('Error fetching user info:', error);
                        alert('No se pudo realizar la reserva.');
                    });
            } else {
                guardarReserva(name, activities, date, time);
            }
        }
    });

    function guardarReserva(name, activities, date, time) {
        const reservation = { name, activities, date, time };

        fetch('http://127.0.0.1:8000/api/reservations/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reservation)
        })
            .then(response => response.json())
            .then(data => {
                alert('Reserva guardada!');
                localStorage.setItem('reservation', JSON.stringify(data));
                document.getElementById('reservation-form').reset();
            })
            .catch(error => {
                console.error('Error saving reservation:', error);
                alert('No se pudo realizar la reserva.');
            });
    }
});
