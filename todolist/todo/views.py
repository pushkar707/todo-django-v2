from django.shortcuts import render
from rest_framework.views import APIView
from todo.serializers import TodoSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from todo.models import Todo
from datetime import datetime


class TodoApi(APIView):
    def post(self, request):
        data = request.data
        serializer = TodoSerializer(
            data=data, context={'user': request.custom_user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.custom_user
        if user.is_superuser:
            todos = Todo.objects.prefetch_related(
                'labels').filter(created_on__date=datetime.now())
        else:
            todos = Todo.objects.prefetch_related(
                'labels').filter(user=user.id, created_on__date=datetime.now())

        serializer = TodoSerializer(instance=todos, many=True)
        return Response({'status': True, 'message': 'Todos fetched', 'data': serializer.data})


class SingleTodoApi(APIView):
    def patch(self, request, id):
        user = request.custom_user
        data = request.data
        if user.is_superuser:
            todo = get_object_or_404(Todo, id=id)
        else:
            todo = get_object_or_404(Todo, user=user, id=id)

        serializer = TodoSerializer(todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = request.custom_user
        if user.is_superuser:
            get_object_or_404(Todo, id=id).delete()
        else:
            get_object_or_404(Todo, user=user, id=id).delete()
        return Response({'status': True, 'message': f'Todo {id} deleted successfully'}, status=status.HTTP_200_OK)
