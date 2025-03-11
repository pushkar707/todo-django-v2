from django.contrib import admin
from todo.models import Todo, Label, BanWords
# Register your models here.


class BanWordsAdmin(admin.ModelAdmin):
    list_display = ['word']
    search_fields = ['word']


class LabelAdmin(admin.ModelAdmin):
    list_display = ['label']
    search_fields = ['label']


class TodoAdmin(admin.ModelAdmin):
    list_display = ['heading', 'description', 'status', 'created_on']
    search_fields = ['heading', 'description']
    list_filter = ['status']
    ordering = ['created_on']
    readonly_fields = ['created_on', 'started_on', 'completed_on']


admin.site.register(BanWords, BanWordsAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Todo, TodoAdmin)
