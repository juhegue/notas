function inicia_cargando() {
    $('#id_cargando').modal('show');
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function funcionAjax(url, param, data) {
	var csrftoken = $.cookie('csrftoken');
    var json = JSON.stringify(param);
    var mitimer = setTimeout(function(){ inicia_cargando(); }, 300);

    param = [{name:'param', value:json}];

	$.ajax({
		async: true,
        contentType: 'application/x-www-form-urlencoded',
		data: param,
        dataType: 'html',
        global: true,
        ifModified: false,
        processData:true,
        timeout: 0,
		type: 'post',
		url: url,

        beforeSend: function(xhr, settings){
        	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
		},
        complete: function(obj, estado) {
            clearTimeout(mitimer);
            $('#id_cargando').modal('hide');
            if(estado=='success'){}
        },
        error: function(obj, estado, error){
        	if (error != '') {
        		alert(estado + ':[' + error + ']');
        		console.log(estado);
        	}
        },
		success:  function(resul, estado, xhr) {
		    if (data == null) {

		    } else {
                if (typeof data === 'string') {
                    $('#' + data).html(resul);

                } else if (typeof data === 'function') {
                    var obj = JSON.parse(resul);
                    if (obj.hasOwnProperty('err') && obj.err) {
                        alert(obj.err);
                    } else {
                        data(obj.param, estado, xhr);
                    }
                } else {
                    for (var i=0; i < data.length; i++){
                        $('#' + data[i]).html(resul);
                    }
                }
            }
		}
	});
}
