$(function() {
    // Este solo afecta a los select2 del modal 
    // $('.select2').select2({
    //     theme: "bootstrap4",
    //     language: 'es',
    //     dropdownParent: $('#modal-movimiento')
    // });


    $('#modal-movimiento .select2').select2({
        theme: "bootstrap4",
        language: 'es',
        dropdownParent: $('#modal-movimiento')
    });
    
    filtrar_area_solicitante();
    
});