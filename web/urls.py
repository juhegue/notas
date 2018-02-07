# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from django.urls import re_path

from .views.inicio import Index
from .views.listanota import ListaNotaView
from .views.iframe import IframeView
from .views.libro import LibroCreateView
from .views.nota import NotaCreateView
from .views.nota import NotaUpdateView
from .views.nota import NotaDeleteView
from .views.ajax import AjaxView
from .views.adjunto import AdjuntoSubir
from .views.adjunto import AdjuntoBajar

# https://simpleisbetterthancomplex.com/references/2016/10/10/url-patterns.html

urlpatterns = [
    # Login / Logout
    re_path(r'^login/$', login, {'template_name': 'web/login.html', }, name="login"),
    re_path(r'^logout/$', logout, {'next_page': '/login/'}, name="logout"),

    # Indice
    re_path(r'^$', Index.as_view(), name="index"),

    re_path(r'^listanota(?:/(?P<libro>\d+))?/$', ListaNotaView.as_view(), name="listanota"),

    re_path(r'^iframe(?:/(?P<id>\d+))?/$', IframeView.as_view(), name="iframe"),

    re_path(r'^libro/nuevo/$', LibroCreateView.as_view(), name="libro_nuevo"),

    re_path(r'^nota/nuevo(?:/(?P<libro>\d+))?/$', NotaCreateView.as_view(), name="nota_nuevo"),
    re_path(r'^nota/editar/(?P<pk>\d+)/$', NotaUpdateView.as_view(), name='nota_editar'),
    re_path(r'^nota/eliminar/(?P<pk>\d+)/$', NotaDeleteView.as_view(), name='nota_eliminar'),

    # Adjuntos
    re_path(r'^adjunto_subir/$', AdjuntoSubir.as_view()),
    re_path(r'^adjunto_bajar/(?P<adj_id>\d+)/$', AdjuntoBajar.as_view()),

    # Ajax
    re_path(r'^getdatos_ajax/([^/]+)', AjaxView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
