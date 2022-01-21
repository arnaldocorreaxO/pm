var anho;
var usu_denom_corta;
var fecha_hora_actual;
var fecha_actual;
var mes_actual;
var anho_actual;


function load() {
    args = []

    usu_denom_corta = $('input[name="usu_denom_corta"]').val();
    fecha_hora_actual = $('input[name="fecha_hora_actual"]').val();
    fecha_actual = $('input[name="fecha_actual"]').val();
    mes_actual = $('input[name="mes_actual"]').val();
    anho_actual = $('select[name="anho"]').val();

    args.push(usu_denom_corta);
    args.push(fecha_hora_actual);
    args.push(fecha_actual);
    args.push(mes_actual);
    args.push(anho_actual);  

    // console.log(anho_actual);

    get_graph_1(args);
    get_graph_2(args);
    get_graph_3(args);
    get_graph_4(args);
    get_graph_5(args);
};


$(function () {


    /*ESTABLECER EL ANHO ACTUAL EN EL DASHBOARD */
    // anho_actual = $('input[name="anho_actual"]').val(); 
    anho = $('select[name="anho"]');    

    /*AL CAMBIAR EL AÑO*/
    anho.on('change', function () {        
        load();
    });

    /*Ambos metodos funciona */
    // anho.val(anho_actual).trigger("change"); //Cambia valor y dispara el evento
    anho.val(anho.val()).change(); //Cambia valor y dispara el evento 


});