$(function() { 

    //SELECT2
    $('#frmModalMovimiento .select2').select2({
        theme: "bootstrap4",
        language: 'es',
        dropdownParent: $('#frmModalMovimiento')
    });

    filtrar_area_solicitante();
    valores_por_defecto();
    validar_formulario();

    function valores_por_defecto() {
        // SUCURSAL POR DEFECTO    
        var action = $('#frmModalMovimiento input[name="action"]').val();
        var sucursal_id = $('#frmModalMovimiento input[name="sucursal_id"]').val();
        var fecha_actual = $('#frmModalMovimiento input[name="fecha_actual"]').val();    
        if (action == 'add') {
            var sucursal = $('#frmModalMovimiento select[name="sucursal"]');
            sucursal.val(sucursal_id).change();
        };        
        // FECHA DATETIMEPICKER
        var fecha = $('#frmModalMovimiento input[name="fecha"]');
        (fecha.val() == '' ? fecha.val(fecha_actual) : 0)
        fecha.daterangepicker({
            language: 'auto',
            singleDatePicker: true,
            showDropdowns: true,
            minYear: 1901,
            // startDate: fecha.val(),
            locale: {
                format: 'DD/MM/YYYY',
            }
        });
    };
 
});

