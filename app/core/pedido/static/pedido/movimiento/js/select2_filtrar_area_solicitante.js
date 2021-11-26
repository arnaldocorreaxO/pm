
function filtrar_area_solicitante() {

    // FILTRAR AREA SOLICITANTE POR DEPARTAMENTO SELECCIONADO
 
    var select_solicitante = $('select[name="solicitante"]');
    var select_area_solicitante = $('select[name="area_solicitante"]');
    var token = $('input[name="csrfmiddlewaretoken"]');

        select_solicitante.on('change', function () {
            /*Cuando el objecto select es multiple retorna un array []
            Si utilizamos select_cliente.val()            retorna la variable cliente[]=[''] Ej. cadena vacía
            Utilizamos    select_cliente.val().join(", ") retorna la variable cliente  =[''] Ej. cadena vacía      
            */
            // typeof [1,2,3,4]              // Returns "object" 
            id_solicitante = $(this).val();
            //Al enviar select multiple 
            if (typeof (id_solicitante) === 'object') {
                id_solicitante = id_solicitante.join(", ");
            };
            
            var options = '<option value="">--------------</option>';
            if (id_solicitante === '') {
                select_area_solicitante.html(options);
                return false;
            };
            $.ajax({
                headers: { "X-CSRFToken": token.val() },
                // url: window.location.pathname,
                url: '/pedido/movimiento',
                type: 'POST',
                data: {
                    'action': 'search_area_solicitante_id',
                    'id': id_solicitante,
                },
                dataType: 'json',
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    select_area_solicitante.html('').select2({
                        theme: "bootstrap4",
                        language: 'es',
                        data: data
                    });
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
                //select_producto.html(options);
            });
        });
};