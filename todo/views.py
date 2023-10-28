from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import TodoItem
from rest_framework import generics
from .serializers import *

# Create your views here.

def addTask(request):
   task=request.POST['task']
   TodoItem.objects.create(title=task,)
   return redirect('home')

def mark_as_done(request,pk):
   task=get_object_or_404(TodoItem,pk=pk)
   task.completed=True
   task.save()
   return redirect('home')

def edit_task(request, pk):
    get_task = get_object_or_404(TodoItem, pk=pk)
    print(get_task)
    if request.method == 'POST':
        new_task = request.POST['task']
        print(new_task)
        get_task.title= new_task
        get_task.save()
        return redirect('home')
    else:
        context = {
            'get_task': get_task,
        }
        return render(request, 'edit_task.html', context)

   

def delete_task(request,pk):
   task=get_object_or_404(TodoItem,pk=pk)
   task.delete()
   return redirect('home')


#CRUD_API

class ListTodo(generics.ListAPIView):
    queryset=TodoItem.objects.all()
    serializer_class=ToDoSerializer

class DetailTodo(generics.RetrieveUpdateAPIView):
    queryset=TodoItem.objects.all()
    serializer_class=ToDoSerializer

class CreateTodo(generics.CreateAPIView):
    queryset=TodoItem.objects.all()
    serializer_class=ToDoSerializer

class DeleteTodo(generics.DestroyAPIView):
    queryset=TodoItem.objects.all()
    serializer_class=ToDoSerializer
