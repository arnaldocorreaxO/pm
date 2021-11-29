$(function() { 

    //SELECT2
    $('#modal-movimiento .select2').select2({
        theme: "bootstrap4",
        language: 'es',
        dropdownParent: $('#modal-movimiento')
    });

    filtrar_area_solicitante();
    valores_por_defecto();
    validar_formulario();

});