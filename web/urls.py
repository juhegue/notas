# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from .views.inicio import Index
from .views.listanota import ListaNotaView, NotasView, LibrosView
from .views.libro import LibroCreateView
from .views.libro import LibroUpdateView
from .views.libro import LibroDeleteView
from .views.nota import NotaCreateView
from .views.nota import NotaUpdateView
from .views.nota import NotaDeleteView
from .views.nota import NotaEnviarView
from .views.nota import NotaDownloadZip
from .views.adjunto import AdjuntoSubir
from .views.adjunto import AdjuntoBajar
from .views.adjunto import AdjuntoBorrar
from .views.cambiaeditor import CambiaEditorView
from .views.calendario import CalendarioView
from .views.eventoPredefinido import EventoPredefinidoCreateView, EventoPredefinidoDeleteView, \
    EventoPredefinidoUpdateView, EventoPredefinidoListView
from .views.resetpassword import RestablecerClave

# https://simpleisbetterthancomplex.com/references/2016/10/10/url-patterns.html

urlpatterns = [
    # Login / Logout
    re_path(r'^login/$',  auth_views.LoginView.as_view(template_name='web/login.html', extra_context={"login": True}), name="login"),
    # re_path(r'^logout/$', auth_views.LogoutView.as_view(template_name='web/logout.html'), name="logout"),

    # Indice
    re_path(r'^$', Index.as_view(), name="index"),

    re_path(r'^listanota(?:/(?P<del_cookie>\d+))?/$', ListaNotaView.as_view(), name="listanota"),

    re_path(r'^libro/nuevo/$', LibroCreateView.as_view(), name="libro_nuevo"),
    re_path(r'^libro/editar/(?P<pk>\d+)/$', LibroUpdateView.as_view(), name="libro_editar"),
    re_path(r'^libro/eliminar/(?P<pk>\d+)/$', LibroDeleteView.as_view(), name="libro_eliminar"),
    re_path(r'^libros/$', LibrosView.as_view(), name='libros'),

    re_path(r'^nota/nuevo(?:/(?P<libro>\d+))?/$', NotaCreateView.as_view(), name="nota_nuevo"),
    re_path(r'^nota/editar/(?P<pk>\d+)/$', NotaUpdateView.as_view(), name='nota_editar'),
    re_path(r'^nota/eliminar/(?P<pk>\d+)/$', NotaDeleteView.as_view(), name='nota_eliminar'),
    re_path(r'^nota/download_zip/(?P<pk>\d+)/$', NotaDownloadZip.as_view(), name='nota_download_zip'),
    re_path(r'^nota/enviar/(?P<pk>\d+)/$', NotaEnviarView.as_view(), name='nota_enviar'),
    re_path(r'^notas/$', NotasView.as_view(), name='notas'),

    # Adjuntos
    path('adjunto_subir/', AdjuntoSubir.as_view(), name='adjunto_subir'),
    path('adjunto_borrar/', AdjuntoBorrar.as_view(), name='adjunto_borrar'),
    path('adjunto_bajar/<int:tipo>/<int:adjunto_id>/', AdjuntoBajar.as_view(), name='adjunto_bajar'),

    # Editor
    re_path(r'^editor/(?P<url_origen>[^/]+)/(?P<editor>[^/]+)/$', CambiaEditorView.as_view(), name='editor'),

    # Calendario
    path('calendario', CalendarioView.as_view(), name="calendario"),
    path('calendario/predefinidos/', EventoPredefinidoListView.as_view(), name="evento_predefinido_lista"),
    path('calendario/predefinidos/nuevo/', EventoPredefinidoCreateView.as_view(), name="evento_predefinido_nuevo"),
    path('calendario/predefinidos/edita/<slug:pk>/', EventoPredefinidoUpdateView.as_view(), name="evento_predefinido_edita"),
    path('calendario/predefinidos/elimina/<slug:pk>/', EventoPredefinidoDeleteView.as_view(), name="evento_predefinido_elimina"),

    # Restablecer la contraseña
    path('reset_password/', RestablecerClave.as_view(), name='reset_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='resetpassword/password_reset_new_password.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='resetpassword/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
