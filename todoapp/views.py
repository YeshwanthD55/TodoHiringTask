from django.shortcuts import render
from todo.models import TodoItem

def home(request):
    tasks= TodoItem.objects.filter(completed=False).order_by('-created_at')
    context={
        'tasks':tasks,
    }
    return render(request,'home.html',context)