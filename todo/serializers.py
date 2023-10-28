from rest_framework import serializers
from .models import *

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model=TodoItem
        fields=('id','title','description','completed','created_at')
        