/*
===================================================================
Author: xO
C:\Users\arnaldo\proyectos\electoral\.env\Lib\site-packages\django\
contrib\admin\templates\admin\change_form.html
Se utiliza para modificar el comportamiento de todos los SELECT en 
el Administrador de Django
En ese path se referencia a este js para Select2 Anidado de Barrios 
y Manzanas
====================================================================
*/
$(function () {
    
    // Este solo afecta a los select2 del modal 
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',
        dropdownParent: $('#modal-movimiento')
    });


    // FILTRAR PRODUCTOS POR CLIENTE SELECCIONADO
 
    var select_solicitante = $('select[name="solicitante"]');
    var select_area_solicitante = $('select[name="area_solicitante"]');
    // var select_vehiculo = $('select[name="vehiculo"]');
    var token = $('input[name="csrfmiddlewaretoken"]');
    // alert(token.val())

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
                url: '/pedido/movimiento/add/',
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
        //     var id_vehiculo = $('#id_vehiculo').val(); //ID VEHICULO
        //     $.ajax({
        //         headers: { "X-CSRFToken": token.val() },
        //         // url: window.location.pathname,
        //         url: '/bascula/movimiento/add/',
        //         type: 'POST',
        //         data: {
        //             'action': 'search_peso_tara_interno',
        //             'id': id_vehiculo
        //         },
        //         dataType: 'json',
        //     }).done(function (data) {
        //         if (!data.hasOwnProperty('error')) {
        //             // SOLO INTERNO 
        //             if (id_cliente == 1) {
        //                 $('#id_peso_entrada').val(parseInt(data['peso']));
        //             };
        //             return false;
        //         }
        //         $('#id_vehiculo').val('').change();
        //         $('#id_cliente').val('').change();
        //         message_error(data.error);
        //     }).fail(function (jqXHR, textStatus, errorThrown) {
        //         alert(textStatus + ': ' + errorThrown);
        //     }).always(function (data) {
        //         //select_producto.html(options);
        //     });

        // });

        // select_vehiculo.on('change', function () {
        //     select_cliente.change();
        // });
   

});