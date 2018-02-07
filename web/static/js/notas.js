/* Rellenar de ceros */
function zeroFill( number, width ) {
    width -= number.toString().length;
    if ( width > 0 ) {
        return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
    }
    return number + "";
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
            $elemento = $('#id_lista_adjuntos'+key);
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
        var key = zeroFill(data.nota_id, 6);
        $elemento = $('#id_lista_adjuntos'+key);
        $elemento.html(data.data);
    });
}

var adjuntos_visible = {};

function MuestraAdjuntos(key, estado) {
    if (estado == undefined) {
        if (adjuntos_visible.key) {estado = false;} else {estado = true;};
    }

    if (estado) {
        $('#id_editor' + key).attr('class', 'col-md-9');
        $('#id_adjuntos' + key).show();
    } else {
        $('#id_adjuntos' + key).hide();
        $('#id_editor' + key).attr('class', 'col-md-12');
    }
    adjuntos_visible.key = estado;
}

$(document).ready(function(){
    // los link con 'onclick' activar con espacio o enter
    $(document).on('keyup', 'a' , function (event) {
        var onclick = $(this).attr('onclick');
        if (onclick) {
            if (event.which == 13 || event.which == 32) {
                $(this).trigger('click');
            }
        }
    });
});

