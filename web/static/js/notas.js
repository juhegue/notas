/* Rellenar de ceros */
function zeroFill( number, width ) {
    width -= number.toString().length;
    if ( width > 0 ) {
        return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
    }
    return number + "";
}

function bootstrapTableDelCookie($table) {
    var prefijo = $table.attr('data-cookie-id-table');
    var path = $table.attr('data-cookie-path');
    $.removeCookie(prefijo + '.bs.table.sortOrder', { path: path });
    $.removeCookie(prefijo + '.bs.table.sortName', { path: path });
    $.removeCookie(prefijo + '.bs.table.pageNumber', { path: path });
    $.removeCookie(prefijo + '.bs.table.pageList', { path: path });
    $.removeCookie(prefijo + '.bs.table.searchText', { path: path });
}

function uploadFiles(key, files, csrf_token){
    $('#id_cargando').modal('show');

    var formData = new FormData();
    files.forEach(function(f) {

        formData.append('files', f);
    });
    formData.append('csrfmiddlewaretoken', csrf_token);
    formData.append('nota_id', key);

    $.ajax({
        url: '/adjunto_subir/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data){
            $elemento = $('#id_lista_adjuntos');
            $elemento.html(data);
            $('#id_cargando').modal('hide');
        },
        error: function(e){
            alert('ERROR.');
            $('#id_cargando').modal('hide');
        }
    });
}


function borraAdjunto(adj_id) {
    var url = '/getdatos_ajax/adjunto_borra';
    var param = {adj_id: adj_id};
    funcionAjax(url, param, function(data){
        $elemento = $('#id_lista_adjuntos');
        $elemento.html(data.data);
    });
}

function borraAdjuntoTemporal(adj_id) {
    var url = '/getdatos_ajax/adjunto_borra_temporal';
    var param = {adj_id: adj_id};
    funcionAjax(url, param, function(data){
        $elemento = $('#id_lista_adjuntos');
        $elemento.html(data.data);
    });
}

function temporizador_descarga() {
    if ($.cookie('fileDownload') == 'true') {
        $.removeCookie('fileDownload', { path: '/' });
        $('#id_cargando').modal('hide');
    }  else {
        setTimeout("temporizador_descarga()", 500);
    }
}

function mensajeLoading(message) {
    $('#id_cargando').modal('show');
    if (message) $('#id_cargando_msg').text(message);
    $.removeCookie('fileDownload', { path: '/' });
    setTimeout('temporizador_descarga()', 1000);
}

$(function () {
    $('.hidden-on-load').show();

    // los link con 'onclick' activar con espacio o enter
    $(document).on('keyup', 'a' , function (event) {
        var onclick = $(this).attr('onclick');
        if (onclick) {
            if (event.which == 13 || event.which == 32) {
                $(this).trigger('click');
            }
        }
    });

    /* muestra el mensaje 'data-mensaje' de la clase '.mensaje' en el click*/
    $(document).on('click', '.mensaje', function (e) {
        var msg = $(this).attr('data-mensaje') || "Cargando...";
        mensajeLoading(msg);
    });

        // lenguaje de select2
    try {
        $('select').select2({
            language: "es"
        });
    } catch
    {}
});

