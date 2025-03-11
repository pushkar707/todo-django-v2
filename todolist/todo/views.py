from django.shortcuts import render
from rest_framework.views import APIView
from todo.serializers import TodoSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from todo.models import Todo
from datetime import datetime
from collections import Counter
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from core.models import CustomUser, RoleChoices
from todo.CustomAuthentication import IsLoggedIn, IsAdminUser


class TodoApi(APIView):
    authentication_classes = [IsLoggedIn]

    def post(self, request):
        data = request.data
        serializer = TodoSerializer(
            data=data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        if user.is_superuser:
            todos = Todo.objects.prefetch_related(
                'labels').filter(created_on__date=datetime.now())
        else:
            todos = Todo.objects.prefetch_related(
                'labels').filter(user=user.id, created_on__date=datetime.now())

        serializer = TodoSerializer(instance=todos, many=True)
        return Response({'status': True, 'message': 'Todos fetched', 'data': serializer.data})


class SingleTodoApi(APIView):
    authentication_classes = [IsLoggedIn]

    def patch(self, request, id):
        user = request.user
        data = request.data
        if user.role == RoleChoices.ADMIN:
            todo = get_object_or_404(Todo, id=id)
        else:
            todo = get_object_or_404(Todo, user=user, id=id)

        serializer = TodoSerializer(todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = request.user
        if user.role == RoleChoices.ADMIN:
            get_object_or_404(Todo, id=id).delete()
        else:
            get_object_or_404(Todo, user=user, id=id).delete()
        return Response({'status': True, 'message': f'Todo {id} deleted successfully'}, status=status.HTTP_200_OK)


class GetLogsApi(APIView):
    authentication_classes = [IsAdminUser]

    def get(self, request):
        # users = CustomUser.objects.filter(todos__logs__isnull=False).values('id','todos__logs__word').annotate(count=Count('todos__logs__word'))
        users = CustomUser.objects.filter(todos__logs__isnull=False).values(
            'id').annotate(words=ArrayAgg('todos__logs__word', distinct=False))

        logs = []
        for user in users:
            obj = {'id': user['id'], 'logs': []}
            words_count = Counter(user['words'])
            for word, count in words_count.items():
                obj['logs'].append({'word': word, 'count': count})
            logs.append(obj)
        # logs = defaultdict(list)
        # for user in users:
        #     obj = {'id': user.id, 'logs': []}

        # for user in users:
        #     obj = {'user_id': user.id, 'logs': []}
        #     for todo in user.todos.all():
        #         logs = todo.logs.values('word').annotate(count=Count('word'))
        #     obj['logs'] = list(logs)

        # words = user.todos.logs.all().values_list('word', flat=True)
        # logs[todo.user_id].append(
        #     {'heading': todo.heading, 'description': todo.description, 'words': words})
        return Response({'status': True, 'message': 'Logs fetched successfully', 'data': logs})


class BanUserApi(APIView):
    authentication_classes = [IsAdminUser]

    def delete(self, request, id):
        user = CustomUser.objects.filter(id=id).update(is_active=False)
        if not user:
            return Response({'error': True, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': True, 'message': 'User banned successfully'})
