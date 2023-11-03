


// Función para verificar la conexión
    function verificarConexion() {
        fetch('/verificar_conexion')
            .then(response => response.json())
            .then(data => {
                // Muestra la respuesta en el div "respuesta"
                document.getElementById('respuesta').innerHTML = JSON.stringify(data);
            })
            .catch(error => console.error('Error:', error));
    }

    // Función para guardar un registro
    function guardarRegistro() {
        fetch('/guardar_registro', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            // Muestra la respuesta en el div "respuesta"
            document.getElementById('respuesta').innerHTML = JSON.stringify(data);
        })
        .catch(error => console.error('Error:', error));
    }
