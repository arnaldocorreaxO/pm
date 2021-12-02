
var input_daterange;
var c=0;
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


      $('input[name="habilita_fecha"]').on('click',function(){            
            c++;
            if (c % 2 == 0){
                $('input[name="date_range"]').prop('disabled', true);
                return
            }
            $('input[name="date_range"]').prop('disabled', false);
      });


});