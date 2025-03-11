from django.contrib import admin
from .models import CustomUser, RoleChoices


# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'role', 'is_banned')
    
#     def has_view_permission(self, request, obj=None):
#         return request.user.is_authenticated and request.user.role == RoleChoices.ADMIN

#     def has_module_permission(self, request):
#         return request.user.is_authenticated and request.user.role == RoleChoices.ADMIN


# admin.site.register(CustomUser, CustomUserAdmin)
