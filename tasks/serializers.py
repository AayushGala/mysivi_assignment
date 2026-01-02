from rest_framework import serializers
from .models import Task, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        write_only=True
    )
    
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='REPORTEE'))

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'categories', 
            'assigned_to', 'assigned_to_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert objects to list of names for read operations
        representation['categories'] = [cat.name for cat in instance.categories.all()]
        return representation

    def validate_assigned_to(self, value):
        user = self.context['request'].user
        if user.role == 'MANAGER':
            # Ensure assigned_to is a reportee of this manager
            if value.created_by != user:
                raise serializers.ValidationError("You can only assign tasks to your own reportees.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        
        if user.role == 'REPORTEE':
            # Reportee can only update status to COMPLETED
            
            # If instance exists (Update)
            if self.instance:
                # Check if status is being changed.
                if 'status' in data:
                    if data['status'] != Task.Status.COMPLETED:
                        raise serializers.ValidationError("Reportees can only update status to COMPLETED.")
                
                # Check if other fields are being changed
                for key in data.keys():
                    if key != 'status':
                        raise serializers.ValidationError(f"Reportees cannot update {key}.")
        
        return data

    def _handle_categories(self, task, categories_data):
        category_objs = []
        for cat_name in categories_data:
            cat_obj, created = Category.objects.get_or_create(name=cat_name)
            category_objs.append(cat_obj)
        task.categories.set(category_objs)

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        task = Task.objects.create(**validated_data)
        self._handle_categories(task, categories_data)
        return task

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', None)
        instance = super().update(instance, validated_data)
        
        if categories_data is not None:
             self._handle_categories(instance, categories_data)
             
        return instance
