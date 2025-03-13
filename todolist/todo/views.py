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
from django.db.models import Q, F
from core.models import CustomUser, RoleChoices
from todo.CustomAuthentication import IsLoggedIn
from todo.CustomPermission import IsAdmin, CanCreateTodo


class TodoApi(APIView):
    '''
    APis to create and get all todos
    '''
    authentication_classes = [IsLoggedIn]
    permission_classes = [CanCreateTodo]

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
            status=TodoStatus.WORKING) | Q(is_recurring=True) | Q(due_on__date__gt=date)
        if user.role != RoleChoices.ADMIN:
            query &= Q(user=user.id)
        todos = Todo.objects.prefetch_related('labels').filter(query)

        serializer = TodoSerializer(instance=todos, many=True)
        return Response({'status': True, 'message': 'Todos fetched', 'data': serializer.data})


class SingleTodoApi(APIView):
    '''
    Update or delete single todo
    '''
    authentication_classes = [IsLoggedIn]
    permission_classes = [CanCreateTodo]

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
    '''
    Allow admin to get all logs
    '''
    authentication_classes = [IsLoggedIn]
    permission_classes = [IsAdmin]

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
    '''
    Allow admin to toggle ban on multiple users at once
    '''
    authentication_classes = [IsLoggedIn]
    permission_classes = [IsAdmin]

    def patch(self, request):
        data = request.data
        ids = data.get('ids')
        user = CustomUser.objects.filter(
            id__in=ids).update(is_banned=~F('is_banned'))

        if not user:
            return Response({'error': True, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': True, 'message': 'Users ban status updates successfully'})
