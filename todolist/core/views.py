from rest_framework.views import APIView
from core.serializers import RegisterSerializer, LoginSerializer, RefreshSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterApi(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(
            data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginApi(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(
            data=data, context={'request': self.request})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RefreshApi(APIView):
    def post(self, request):
        data = request.data
        serializer = RefreshSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
