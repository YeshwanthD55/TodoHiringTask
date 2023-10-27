from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import TodoItem

# Create your views here.

def addTask(request):
   task=request.POST['task']
   TodoItem.objects.create(title=task,)


   return redirect('home')