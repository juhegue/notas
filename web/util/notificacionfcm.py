# -*- coding: utf-8 -*-

import os
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

from django.conf import settings

logger = logging.getLogger(__name__)


server_key = os.path.join(settings.BASE_DIR, 'notas', 'notas-notifica-firebase-adminsdk-9gsx1-76cf0d1ab9.json')
cred = credentials.Certificate(server_key)
firebase_admin.initialize_app(cred)


class NotificacionFcm(object):
    def __init__(self, usuario):
        self.usuario = usuario

    def _envia(self, msg_title, msg_body, data_extra=None):
        fcm_token = self.usuario.fcm_token
        if fcm_token and self.usuario.is_active:
            try:
                message = messaging.MulticastMessage(
                    notification=messaging.Notification(
                        title=msg_title,
                        body=msg_body
                    ),
                    tokens=[fcm_token]
                )
                if data_extra:
                    message.data = data_extra

                response = messaging.send_each_for_multicast(message)
                logger.info("NotificacionFcm[RESULT]: %s" % response)

            except Exception as e:
                logger.error("NotificacionFcm[ERROR]: %s" % e)

    def demo(self):
        title = 'Demo de notas_notifica'
        body = '¡Hola Mundo, esto solo es una prueba!'
        self._envia(title, body)

    def aviso(self, title, body):
        self._envia(title, body)
