from django.contrib import admin
from .models import CustomUser
from django.db.models import Count


@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'email',
                    'is_banned', 'todos_count', 'logs_count']

    # Show total todos created by a user
    @admin.display(description='Todos Count')
    def todos_count(self, instance):
        return instance.todos_count

    # Shows total logs created due to ban words usage by a user
    @admin.display(description='Logs Count')
    def logs_count(self, instance):
        return instance.logs_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(todos_count=Count('todos'),
                                 logs_count=Count('todos__logs'))


# admin.site.register(CustomUser, AdminUser)
