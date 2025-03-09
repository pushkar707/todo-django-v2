from django.urls import path
from todo.views import TodoApi, SingleTodoApi

urlpatterns = [
    path('', TodoApi.as_view()),
    path('<int:id>/', SingleTodoApi.as_view())
]
