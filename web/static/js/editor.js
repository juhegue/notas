//http://www.codingdrama.com/bootstrap-markdown/

function showEditor(nota_id, btn_grabar, initialstate){
    var hiddenButtons = [];
    if (!btn_grabar) hiddenButtons.push('cmdGrabar');

    $('#id_teditor' + nota_id).markdown({
        window: null,
        initialstate: initialstate,
        hiddenButtons: hiddenButtons,
        iconlibrary : 'fa',
        language:'es',
        autofocus:false,
        savable:false,
        onShow: function(e){
//            if (this.initialstate === 'preview') $('.btn-toolbar').hide();
        },
        onFocus: function(e){
/*
            if (this.initialstate === 'preview') {
                this.initialstate = 'editor';
                $('.btn-toolbar').show();
                e.hidePreview();
            }
*/
        },
        hiddenButtons: hiddenButtons,
        additionalButtons: [
            [{
                  name: "groupUtil",
                  data: [{
                            name: "cmdImprimir",
                            toggle: false,
                            title: "Imprimir",
                            icon: {glyph: 'glyphicon glyphicon-print',
                                   fa: 'fa fa-file-pdf-o'
                            },
                            callback: function(e){
                                var html = e.parseContent();
                                var doc = new jsPDF();
                                doc.fromHTML(html, 10, 10);
                                doc.save(nota_id)
                            }
                        }]
            },
            {
                  name: "groupCustom1",
                  data: [{
                            name: "cmdAdjunto",
                            toggle: true,
                            title: "Adjuntos",
                            icon: {glyph: 'glyphicon glyphicon-file',
                                   fa: 'fa fa-paperclip'
                            },
                            callback: function(e){
                                parent.MuestraAdjuntos(nota_id);
                            }
                        }]
            },
            {
                  name: "groupCustom2",
                  data: [{
                            name: "cmdGuia",
                            toggle: false,
                            title: "Guia Markdawn",
                            icon: {glyph: 'glyphicon glyphicon-info-sign',
                                   fa: 'fa fa-info-circle'
                            },
                            callback: function(e){
                                window.open('/guia_markdawn/', '_blank');
                            }
                        }]
            },
            {
                  name: "groupCustom3",
                  data: [{
                            name: "cmdGrabar",
                            toggle: false,
                            title: "Grabar",
                            icon: {glyph: 'glyphicon glyphicon-floppy-saved',
                                   fa: 'fa fa-floppy-o'
                            },
                            btnClass: 'btn btn-primary btn-sm',
                            btnText: 'Grabar',
                            callback: function(e){
                                var texto = e.getContent();
                                var html = e.parseContent();
                                var url = '/getdatos_ajax/graba_nota_texto';
                                var param = {nota_id: nota_id, texto: texto, html: html};
                                funcionAjax(url, param, function(data){
                                    $el = $('#id_editor' + nota_id).find('[data-handler="bootstrap-markdown-cmdGrabar"]');
                                    $el.popover({
                                        trigger: 'manual',
                                        animation: true,
                                        placement: 'down',
                                        content: ''
                                    });
                                    $el.popover('show');
                                    setTimeout(function(){$el.popover('destroy');}, 300);
                                });
                            }
                        },/* {
                            name: "cmdBeer",
                            toggle: true, // this param only take effect if you load bootstrap.js
                            title: "Beer",
                            icon: {glyph: 'glyphicon glyphicon-file'},
                            callback: function(e){}
                        }*/],
            }]
        ]
    })
}
