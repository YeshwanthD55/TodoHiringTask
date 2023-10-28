from django.urls import path
from . import views
from .views import DetailTodo,ListTodo,CreateTodo,DeleteTodo

urlpatterns=[
    path('addTask/',views.addTask,name='addTask'),
    path('mark_as_done/<int:pk>/',views.mark_as_done,name='mark_as_done'),
    path('edit_task/<int:pk>/',views.edit_task,name='edit_task'),
    path('delete_task/<int:pk>/',views.delete_task,name='delete_task'),

    path('<int:pk>/',DetailTodo.as_view()),
    path('',ListTodo.as_view()),
    path('create',CreateTodo.as_view()),
    path('delete/<int:pk>',DeleteTodo.as_view())
]