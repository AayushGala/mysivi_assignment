from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'created_at', 'updated_at']

class ManagerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    def create(self, validated_data):
        validated_data['role'] = User.Role.MANAGER
        user = User.objects.create_user(**validated_data)
        return user

class CreateReporteeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        # Role logic handled here or in view. Better in view or here.
        # Requirements says Manager creates Reportee.
        validated_data['role'] = User.Role.REPORTEE
        return User.objects.create_user(**validated_data)
