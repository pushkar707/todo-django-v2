from django.urls import path, include

urlpatterns = [
    path('auth/', include('core.urls')),
    path('todos/', include('todo.urls'))
]
