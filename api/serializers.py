from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_admin']
        extra_kwargs = {
            'password':{'write_only':True},
            'email':{'required':True}
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email')
        validated_data['username'] = email  # Set username as email
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin']