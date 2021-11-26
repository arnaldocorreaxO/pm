var tblData;
var input_daterange;
var columns = [];

function init() {
    // Este es para los select2 de la lista no afecta al modal 
    // Para el modal ver el comentario en del javascript
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',
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
        select_anho.val("").change();
        select_solicitante.val("").change();
        select_area_solicitante.val("").change();
        // select_seccional.val("").change();
        // select_barrio.val("").change();
        // select_manzana.val("").change();
        // select_mesa.val("").change();
        // select_pasoxpc.val("").change();
        // select_pasoxmv.val("").change();
    }

    var parameters = {
        'action': 'search',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        'term': input_term.val(),
        'anho': select_anho.val().join(", "),
        'solicitante': select_solicitante.val().join(", "),
        'area_solicitante': select_area_solicitante.val().join(", "),
        // 'barrio': select_barrio.val(),
        // 'manzana': select_manzana.val(),
        // 'mesa': select_mesa.val(),
        // 'pasoxpc': select_pasoxpc.val(),
        // 'pasoxmv': select_pasoxmv.val(),
        
    };

    if (all!='bday') {
        parameters['start_date'] = '';
        parameters['end_date'] = '';
    }
    
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
                   
                //    var badge_pc = '<span class="badge badge-warning">' + ' PC ' + '</span>';
                //    var badge_mv = '<span class="badge badge-success">' + ' SI ' + '</span>';
                //    var badge_no = '<span class="badge badge-danger"> NO </span>';
                //    var badges = badge_no; /*Default*/
                    
                //         if (row.pasoxpc =='S') {
                //             badges = badge_pc  + badge_no;
                //         }
                //         if (row.pasoxmv =='S') {
                //             badges = badge_mv;
                //             if (row.pasoxpc =='S') {
                //                 badges = badge_pc  + badge_mv;
                //             }
                //         }     
                //         if (row.tipo_voto.id == 11){
                //            return '<span class="badge badge-secondary">'+ row.tipo_voto.cod +'</span>';
                //         }                  
                     
                //      return badges;
                return data;
                }         
            },
            {
                targets: [3],
                class: 'text-left',
                render: function (data, type, row) {                   

                        // if (row.tipo_voto.id == 1) {
                        //     return '<span class="badge badge-danger">' + data + '</span>'
                        // }
                        // if (row.tipo_voto.id == 2) {
                        //     return '<span class="badge badge-info">' + data + '</span>'
                        // }
                        // if (row.tipo_voto.id == 3) {
                        //     return '<span class="badge badge-dark">' + data + '</span>'
                        // }
                        // if (row.tipo_voto.id == 4) {
                        //     return '<span class="badge badge-success">' + data + '</span>'
                        // }
                        // // Ausentes
                        // if (row.tipo_voto.id == 13){
                        //     return '<span class="badge badge-warning">'+ data +'</span>';
                        //  }   
                        // //  Fallecidos
                        //  if (row.tipo_voto.id == 11){
                        //     return '<span class="badge badge-secondary">'+ data +'</span>';
                        //  }   
                        // //Otros
                        return data;
                        
                }         
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';                    
                    buttons += '<button type="button" class="btn btn-warning js-update" data-url="/pedido/movimiento/update/' + row.id + '/"><i class="fas fa-edit"></i></button>';
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
}

// INIT LOAD
$(function () {  

    // var link_add = document.querySelector('a[href="/electoral/elector/add/"]');
    // var link_upd = document.querySelector('a[href=""]');
    // link_add.style.display = 'none';
    // link_upd.style.display = 'none';

    input_term = $('input[name="term"]');
    current_date = new moment().format('YYYY-MM-DD');
    input_daterange = $('input[name="date_range"]');    
    select_anho = $('select[name="anho"]');
    select_solicitante = $('select[name="solicitante"]');
    select_area_solicitante = $('select[name="area_solicitante"]');
    // select_seccional = $('select[name="seccional"]');
    // select_barrio = $('select[name="barrio"]');
    // select_manzana = $('select[name="manzana"]');
    // select_mesa = $('select[name="mesa"]');
    // select_pasoxpc = $('select[name="pasoxpc"]');
    // select_pasoxmv = $('select[name="pasoxmv"]');


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
    getData('all');

    $('.btnSearch').on('click', function () {
        getData('bday');
    });

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

    //  select_ciudad.val("").change();
    //  select_seccional.val("").change();
    //  select_barrio.val("").change();
    //  select_manzana.val("").change();
    //  select_mesa.val("").change();

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
                $("#modal-movimiento").modal("show");
            },
            success: function (data) {
                // console.log('SUCEEEEEEEEEEEEEEEEEEEEEEEEESS')   
                if (!data.hasOwnProperty('error')) {
                    $("#modal-movimiento .modal-content").html(data.html_form);
                    return false;
                }
                console.log(data);
                message_error(data.error);
            }
        });
    };
  
    var saveForm = function () {
        // Habilitamos antes de submit
        // var select_seccional = $('#frmForm #id_seccional')
        // var select_local_votacion = $('#frmForm #id_local_votacion')
        // select_seccional.prop("disabled", false);
        // select_local_votacion.prop("disabled", false);


        var form = $(this);        
            $.ajax({
                url: form.attr("action"),
                data: form.serialize(),
                type: form.attr("method"),
                dataType: 'json',
                success: function (request) {
                    // console.log(request);
                    if (!request.hasOwnProperty('error')) {   
                        tblData.draw('page');
                        $("#modal-movimiento").modal("hide");
                        // select_seccional.prop("disabled", true);
                        // select_local_votacion.prop("disabled", true); 
                        message_success('Guardado Exitosamente!')                                               
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
   
    /* Binding */
  
    // Create Movimiento Pedido
    $(".js-create").click(loadForm);
    $("#modal-movimiento").on("submit", ".js-create-form", saveForm);
  
    // Update Movimiento Pedido
    $("#data").on("click", ".js-update", loadForm);
    $("#modal-movimiento").on("submit", ".js-update-form", saveForm);
  
  });