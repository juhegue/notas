var timer_ajax;

function inicia_cargando() {
    if (timer_ajax) {
        $('#id_cargando').modal('show', function() {
            if (!timer_ajax)
                $('#id_cargando').modal('hide');
        });
    }
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}


function funcionAjax(url, param, data, timer) {
    var timer = (typeof timer === 'undefined') ? true : timer;
	var csrftoken = getCookie('csrftoken');
	var cursores = {}

    var json = JSON.stringify(param);
    param = [{name:'param', value:json}];
    timer_ajax = timer;
    if (timer) var mitimer = setTimeout(function(){ inicia_cargando(); }, 1000);

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
        	if (!csrfSafeMethod(settings.type) && !this.crossDomain && sameOrigin(settings.url)) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
		},
        complete: function(obj, estado) {
            if (timer) clearTimeout(mitimer);
            $('#id_cargando').modal('hide');
            timer_ajax = false;
            if(estado=='success'){}
        },
        error: function(obj, estado, error){
        	if (error != '') {
        		alert(estado + ':[' + error + ']');
        		console.log(estado, error, json);
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
                        //if (obj.hasOwnProperty('msg') && obj.msg != '') { alert(obj.msg); }
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
