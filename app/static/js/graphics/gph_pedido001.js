
function get_graph_1(args) {
    anho = args[4]
    var graph_1 = Highcharts.chart('graph_1', {
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        exporting: {
            enabled: true
        },
        title: {
            text: '</i><span style="font-size:20px; font-weight: bold;">Situación Pedidos Año: ' + anho + '</span>'
        },
        subtitle: {
            text: args[0] + '<br> Actualizado: ' + args[1]
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        tooltip: {
            pointFormat: 'Total: <b>{point.y:.0f} UND.</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.2f} %'
                }
            }
        },
    });

    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'anho': anho,
            'action': 'get_graph_1',

        },
        dataType: 'json',
    }).done(function (request) {
        if (!request.hasOwnProperty('error')) {
            graph_1.addSeries(request);
            return false;
        }
        message_error(request.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}