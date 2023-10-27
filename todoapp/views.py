from django.shortcuts import render
from todo.models import TodoItem

def home(request):
    tasks= TodoItem.objects.filter(completed=False).order_by('-created_at')
    completed_tasks = TodoItem.objects.filter(completed=True)
    context={
        'tasks':tasks,
        'completed_tasks':completed_tasks,
    }
    return render(request,'home.html',context)