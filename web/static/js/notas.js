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

function adjuntoHtml(data, nota_id){
    var html = '<div class="card"><table class="table" style="width:100%">',
        tipo;

    for (var i=0; i<data.length; i++) {
        (data[i].tmp) ? tipo=0: tipo=1;
        html += sprintf(`
            <tr>
                <td class="text-center" style="width:10px">
                    <a href="javascript:adjElimina(%s,%s,%s);" class="text-danger" role="button"><span class="fa fw fa-trash"></span></a>
                </td>
                <td class="wrappable">
                    <a href="/adjunto_bajar/%s/%s/">%s</a>
                </td>
            </tr>
        `, tipo, data[i].id, nota_id
         , tipo, data[i].id, data[i].nombre);
    }
    html += '</table></div>';
    return html;
}

function ajax(url, formData, nota_id){
    //$('#id_cargando').modal('show');
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        dataType: 'JSON',
        processData: false,
        contentType: false,
        success: function(data){
            var $elemento = $('#id_lista_adjuntos'),
                html = adjuntoHtml(data, nota_id);
            $elemento.html(html);
            $('#id_cargando').modal('hide');
        },
        error: function(e){
            alert('ERROR.');
            $('#id_cargando').modal('hide');
        }
    });
}

function uploadFiles(csrf_token, nota_id, uuid_id, files){
    $('#id_cargando').modal('show');

    var formData = new FormData();
    formData.append('nota_id', nota_id);
    formData.append('uuid_id', uuid_id);
    files.forEach(function(f) {
        formData.append('files', f);
    });
    formData.append('csrfmiddlewaretoken', csrf_token);
    ajax('/adjunto_subir/', formData, nota_id);
}

function adjuntoBorra(csrf_token, nota_id, uuid_id, adjunto_id, tipo) {
    var formData = new FormData();
    formData.append('tipo', tipo);
    formData.append('csrfmiddlewaretoken', csrf_token);
    formData.append('uuid_id', uuid_id);
    formData.append('adjunto_id', adjunto_id);
    formData.append('nota_id', nota_id||0);
    ajax('/adjunto_borrar/', formData, nota_id);
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

function marca1Imput() {    // marca 1º imput
    $('input, select, textarea').each(function(){
        var $this = $(this),
            id = $this.attr('id');

        if (id && !$this.is('[readonly]') && $this.is(':visible') && !$this.is(':disabled')) {
            if($this.is("select")) {
                $this.select2('open');
                $this.select2('close');
            } else {
                $this.focus().select();
            }
            return false;
        }
    });
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
        var msg = $(this).attr('data-mensaje') || "Procesando...";
        mensajeLoading(msg);
    });

        // lenguaje de select2
    try {
        $('select').select2({
            language: "es"
        });
    } catch {
    }

    setTimeout(function(){
        marca1Imput();
    }, 100);

});

