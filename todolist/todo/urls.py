from django.urls import path
from todo.views import TodoApi, SingleTodoApi, GetLogsApi, BanUserApi

urlpatterns = [
    path('', TodoApi.as_view()),
    path('<int:id>/', SingleTodoApi.as_view()),
    path('logs/', GetLogsApi.as_view()),
    path('ban/<int:id>', BanUserApi.as_view())
]
