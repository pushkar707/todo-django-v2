from django.contrib import admin
from todo.models import Todo, Label, BanWords
# Register your models here.

admin.site.register([Todo, Label, BanWords])
