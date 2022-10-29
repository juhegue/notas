# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from post_office import mail
from web.models import AgendaEvento
from web.util.notificacionfcm import NotificacionFcm

HORAS_MARGEN_COMPLETO = 12
MINUTOS_MARGEN_PARCIAL = 30


def envia_movil(qevento):
    inicio = timezone.localtime(qevento.inicio).strftime('%H:%M')
    finhora = timezone.localtime(qevento.fin).strftime('%H:%M')
    fin = timezone.localtime(qevento.fin).strftime('%d/%m/%Y %H:%M')

    periodo = f'Desde {inicio}'
    if qevento.fin:
        if qevento.inicio.date() == qevento.fin.date():
            periodo += f' Hasta {finhora}'
        else:
            periodo += f' Hasta {fin}'

    n = NotificacionFcm(qevento.usuario)
    n.aviso('Notas notifiación', f'{periodo}\n{qevento.titulo}')


def envia_mail(qevento):
    inicio = timezone.localtime(qevento.inicio).strftime('%H:%M')
    finhora = timezone.localtime(qevento.fin).strftime('%H:%M')
    fin = timezone.localtime(qevento.fin).strftime('%d/%m/%Y %H:%M')

    periodo = f'Desde{inicio}'
    if qevento.fin:
        if qevento.inicio.date() == qevento.fin.date():
            periodo += f' Hasta {finhora}'
        else:
            periodo += f' Hasta {fin}'

    mail.send(
        recipients=qevento.usuario.email,
        subject=f'Aviso: {qevento.titulo}',
        message=f'{periodo}\n{qevento.titulo}',
        html_message=f'<h3>{periodo}</h3><br>{qevento.titulo}',
    )


def procesa_eventos():
    ahora = timezone.now()

    inicio = ahora + timedelta(hours=HORAS_MARGEN_COMPLETO)
    for qevento in AgendaEvento.objects.filter(dia_completo=True,
                                               inicio__lte=inicio,
                                               fin__gte=ahora):
        if qevento.aviso_email and not qevento.email_enviado:
            envia_mail(qevento)
            qevento.email_enviado = ahora
            qevento.save()

        if qevento.aviso_movil and not qevento.movil_enviado:
            envia_movil(qevento)
            qevento.movil_enviado = ahora
            qevento.save()

    inicio = ahora + timedelta(minutes=MINUTOS_MARGEN_PARCIAL)
    for qevento in AgendaEvento.objects.filter(dia_completo=False,
                                               inicio__lte=inicio,
                                               fin__gte=ahora):
        if qevento.aviso_email and not qevento.email_enviado:
            envia_mail(qevento)
            qevento.email_enviado = ahora
            qevento.save()

        if qevento.aviso_movil and not qevento.movil_enviado:
            envia_movil(qevento)
            qevento.movil_enviado = ahora
            qevento.save()


def start():     # Añadir el start en apps.py
    scheduler = BackgroundScheduler()
    scheduler.add_job(procesa_eventos, 'interval', minutes=1)
    scheduler.start()
