# -*- coding: utf-8 -*-

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .authentication import token_expire_handler, expires_in


class MiObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # caducidad del token
        is_expired, token = token_expire_handler(token)
        s = expires_in(token)

        return Response({'token': token.key, 'expires_in': str(s).split('.')[0]})


obtain_auth_token = MiObtainAuthToken.as_view()
