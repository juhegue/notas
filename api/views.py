# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status


class FcmSerializerIn(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=400)


class HelloView(views.APIView):

    def get(self, request):
        content = {'message': 'Hola, Mundo!'}
        return Response(content)


class TokenFcmView(views.APIView):

    def post(self, request, *args, **kwargs):
        s = FcmSerializerIn(data=request.data)
        if not s.is_valid():
            response = {"result": "Error", "detail": s.errors}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_active:
            response = {"result": "Error", "detail": "Usuario inactivo."}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        fcm_token = s.validated_data["fcm_token"]

        request.user.fcm_token = fcm_token
        request.user.save()

        response = {
            "result": "Ok",
            "detail": {"fcm_token": fcm_token}
        }
        return Response(response, status=status.HTTP_200_OK)
