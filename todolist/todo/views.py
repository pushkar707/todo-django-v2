from django.shortcuts import render
from rest_framework.views import APIView
from todo.serializers import TodoSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from todo.models import Todo, TodoStatus
from datetime import datetime
from collections import Counter
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from core.models import CustomUser, RoleChoices
from todo.CustomAuthentication import IsLoggedIn, IsAdminUser, CanCreateTodo


class TodoApi(APIView):
    authentication_classes = [IsLoggedIn]

    def get_authenticators(self):
        if self.request.method == 'POST':
            return [CanCreateTodo()]
        return super().get_authenticators()

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
        day = self.request.GET.get('day')
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        date = None
        if day and month and year:
            try:
                date = datetime(int(year), int(month), int(day)).date()
            except ValueError:
                date = datetime.now().date()
        else:
            date = datetime.now().date()
        query = Q(created_on__date=date) | Q(
            status=TodoStatus.WORKING) | Q(is_recurring=True)
        if user.role != RoleChoices.ADMIN:
            query &= Q(user=user.id)
        todos = Todo.objects.prefetch_related('labels').filter(query)

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
        users = CustomUser.objects.filter(todos__logs__isnull=False).values(
            'id').annotate(words=ArrayAgg('todos__logs__word', distinct=False))

        logs = []
        for user in users:
            obj = {'user_id': user['id'], 'logs': []}
            words_count = Counter(user['words'])
            for word, count in words_count.items():
                obj['logs'].append({'word': word, 'count': count})
            logs.append(obj)
        return Response({'status': True, 'message': 'Logs fetched successfully', 'data': logs})


class BanUserApi(APIView):
    authentication_classes = [IsAdminUser]

    def patch(self, request, id):
        user = CustomUser.objects.get(id=id)
        if user.is_banned:
            user.is_banned = False
            message = 'User unbanned successfully'
        else:
            user.is_banned = True
            message = 'User banned successfully'
        user.save()

        if not user:
            return Response({'error': True, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': True, 'message': message})
