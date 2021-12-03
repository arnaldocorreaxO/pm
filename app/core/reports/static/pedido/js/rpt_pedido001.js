
var input_daterange;

// INIT LOAD
$(function () {
    current_date = new moment().format('YYYY-MM-DD');
    input_daterange = $('input[name="date_range"]');
    $('input[name="date_range"]').prop('disabled', true);
    // RANGO DE FECHAS
    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {

        });


        $('input[name="habilita_fecha"]').change(function () {
            if ($(this).prop('checked')) {
                $('input[name="date_range"]').prop('disabled', false);
            } else {
                $('input[name="date_range"]').prop('disabled', true);
            };
        });

      filtrar_area_solicitante();


});