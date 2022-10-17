'use strict';

function bootstrapTableDelCookie($table) {
    var prefijo = $table.attr('data-cookie-id-table');
    var path = $table.attr('data-cookie-path');
    $.removeCookie(prefijo + '.bs.table.sortOrder', { path: path });
    $.removeCookie(prefijo + '.bs.table.sortName', { path: path });
    $.removeCookie(prefijo + '.bs.table.pageNumber', { path: path });
    $.removeCookie(prefijo + '.bs.table.pageList', { path: path });
    $.removeCookie(prefijo + '.bs.table.searchText', { path: path });
/* no funciona!
    $table.bootstrapTable('deleteCookie', 'sortOrder');
    $table.bootstrapTable('deleteCookie', 'sortName');
    $table.bootstrapTable('deleteCookie', 'pageNumber');
    $table.bootstrapTable('deleteCookie', 'pageList');
    $table.bootstrapTable('deleteCookie', 'searchText');
*/
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

function ajaxAdjunto(url, formData, nota_id){
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
            $('#id_cargando').modal('hide');
            alert('ERROR.');
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
    ajaxAdjunto('/adjunto_subir/', formData, nota_id);
}

function adjuntoBorra(csrf_token, nota_id, uuid_id, adjunto_id, tipo) {
    var formData = new FormData();
    formData.append('tipo', tipo);
    formData.append('csrfmiddlewaretoken', csrf_token);
    formData.append('uuid_id', uuid_id);
    formData.append('adjunto_id', adjunto_id);
    formData.append('nota_id', nota_id||0);
    ajaxAdjunto('/adjunto_borrar/', formData, nota_id);
}

$(function () {
    bootbox.setDefaults({
        locale: languageCode,
        show: true,
        closeButton: false,
        animate: true,
    });
    marca1Imput();
});
