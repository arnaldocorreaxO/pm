var tblData;
var columns = [];
function init() {
    $(document).ready(function () {
        $('.select2').select2({
            theme: "bootstrap4",
            language: 'es',

        });
        $('input[name="date_range"]').prop('disabled', true);
        filtrar_area_solicitante();

    });

    tblData = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
        // deferRender: true,
        // processing: true,
        // serverSide: true,
    });

    $.each(tblData.settings()[0].aoColumns, function (key, value) {
        columns.push(value.sWidthOrig);
    });

    $('#data tbody tr').each(function (idx) {
        $(this).children("td:eq(0)").html(idx + 1);
        console.log(idx+1);
    });
}

function getData(all) {
    if (all=='all'){
        input_term.val("");
        select_sucursal.val("").change();
        select_anho.val("").change();
        select_situacion.val("").change();
        select_solicitante.val("").change();        
        select_area_solicitante.val("").change();
    }

    var parameters = {
        'action': 'search',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        'term': input_term.val(), 
        'sucursal': (select_sucursal.val().includes('')?'*':select_sucursal.val().join(", ")),
        'anho':(select_anho.val().includes('')?'*':select_anho.val().join(", ")),
        'situacion': "'"+(select_situacion.val().includes('')?'*':select_situacion.val().join("','"))+"'",
        'solicitante': (select_solicitante.val().includes('')?'*':select_solicitante.val().join(", ")),        
        'area_solicitante': (select_area_solicitante.val().includes('')?'*':select_area_solicitante.val().join(", "))   
    }; 

    if ($('input[name="habilita_fecha"]').prop('checked')!=true) {  
            parameters['start_date']= '';
            parameters['end_date']= '';    
    };


    
    tblData = $('#data').DataTable({        
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        processing: true,
        serverSide: true,
        paging: true,
        ordering: true,
        searching: true,
        // stateSave: true,      Salva la seleccion de longitud de pagina lengthMenu  
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
        pagingType: "full_numbers",
        pageLength: 10,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            // dataSrc: ""
        },
        // order: [[2, 'asc'],[1, 'asc'],[5, 'asc'],[2, 'asc']],
        order: [[1, 'asc'],[0, 'asc']],
        
        
        dom: 'Blfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = columns;
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: current_date}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        columns: [
            // {data: "position"},
            // {data: "id"},         
            {data: "nro_pedido"},
            {data: "fecha"},
            // {data: "nombre"},
            {data: "solicitante_denom_corta"},
            {data: "area_solicitante_denom_corta"},
            {data: "descripcion"},
            {data: "destino"},
            {data: "situacion"},
            {data: "id"},   
        ],
        columnDefs: [
          
            {
                targets: [0],
                class: 'text-center',
                render: function (data, type, row) {                
                          return data;
                }         
            },
            {
                targets: [6],
                class: 'text-center',
                render: function (data, type, row) {
                    switch (row.situacion) {
                        case 'CUMPLIDO':
                            return '<span class="badge badge-success">' + data + '</span>'
                        case 'PARCIAL CUMPLIDO':
                            return '<span class="badge badge-warning">' + data + '</span>'
                        case 'LICITACION':
                            return '<span class="badge badge-info">' + data + '</span>'
                        case 'ADJUDICADO':
                            return '<span class="badge badge-secondary">' + data + '</span>'
                        default:
                            return '<span class="badge badge-danger">PENDIENTE</span>'
                    };
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    console.log(row);
                    var buttons = '';  
                    if (row.sucursal == row.usuario_sucursal){                    
                        // buttons += '<button type="button" class="btn btn-primary js-detail" data-url="/pedido/movimiento/detail/' + row.id + '/"><i class="fas fa-folder-open"></i></button>';
                        buttons += '<button type="button" class="btn btn-warning js-update" data-url="/pedido/movimiento/update/' + row.id + '/"><i class="fas fa-edit"></i></button>';
                    }
                    return buttons;
                }
            },
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {
            $('[data-toggle="tooltip"]').tooltip();
        }
    });
};

// INIT LOAD
$(function () {  
    // var link_add = document.querySelector('a[href="/electoral/elector/add/"]');
    // var link_upd = document.querySelector('a[href=""]');
    // link_add.style.display = 'none';
    // link_upd.style.display = 'none';

    input_term = $('input[name="term"]');
    current_date = new moment().format('YYYY-MM-DD');
    input_daterange = $('input[name="date_range"]');   
    select_sucursal = $('select[name="sucursal"]'); 
    select_anho = $('select[name="anho"]');
    select_situacion = $('select[name="situacion"]');    
    select_solicitante = $('select[name="solicitante"]');
    select_area_solicitante = $('select[name="area_solicitante"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            getData('filter');
        });

    $('.drp-buttons').hide();

    init();
    // getData('all'); 

    $('.btnFilter').on('click', function () {
        getData('filter');
    });

    $('.btnSearchAll').on('click', function () {
        getData('all');
    });

    // BTN DEFAULT 
    input_term.keypress(function(e){
        if(e.keyCode==13)
        $('.btnFilter').click();
      });

});

// VENTANAS MODAL 
$(function () {
    /* Functions */  
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {         
                    $("#frmModalMovimiento").modal("show");
            },
            success: function (data) {
                // console.log('SUCEEEEEEEEEEEEEEEEEEEEEEEEESS')   
                if (!data.hasOwnProperty('error')) {                    
                    $("#frmModalMovimiento .modal-content").html(data.html_form);
                    return false;
                }
                console.log(data);
                message_error(data.error);
            }
        });
    };
  
    var saveForm = function () {
        var form = $(this);  
        // Habilitamos antes de submit 
        $('#frmModalMovimiento select[name="sucursal"]').prop('disabled', false);     
            $.ajax({
                url: form.attr("action"),
                data: form.serialize(),
                type: form.attr("method"),
                dataType: 'json',
                success: function (request) {
                    // console.log(request);
                    if (!request.hasOwnProperty('error')) {   
                        tblData.draw('page');
                        $("#frmModalMovimiento").modal("hide");
                        // select_seccional.prop("disabled", true);
                        // select_local_votacion.prop("disabled", true); 
                        message_success('Guardado Exitosamente!');
                        $('#frmModalMovimiento select[name="sucursal"]').prop('disabled', true);                                                   
                        return false;
                    }
                    message_error(request.error);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    message_error(errorThrown + ' ' + textStatus);
                }
            });
        return false;
    };

    // Create Movimiento Pedido
    $(".js-create").click(loadForm);
    $("#frmModalMovimiento").on("submit", ".js-create-form",saveForm);
  
    // Update Movimiento Pedido
    $("#data").on("click", ".js-update", loadForm);
    $("#frmModalMovimiento").on("submit", ".js-update-form", saveForm);
    
    // Update Movimiento Pedido
    // $("#data").on("click", ".js-detail", loadForm);


    $('input[name="habilita_fecha"]').change(function () {
        if ($(this).prop('checked')) {
            $('input[name="date_range"]').prop('disabled', false);
        } else {
            $('input[name="date_range"]').prop('disabled', true);
        };
    });

    // #SUCURSAL POR DEFECTO 
    var sucursal_id = $('input[name="sucursal_id"]').val();   
    select_sucursal.val(sucursal_id).change();
    // getData('all');
  
  });



  