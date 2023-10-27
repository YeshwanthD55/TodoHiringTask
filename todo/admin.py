from django.contrib import admin
from .models import TodoItem

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display=('title','completed','created_at')
    search_fields=('title',)


admin.site.register(TodoItem,TaskAdmin)