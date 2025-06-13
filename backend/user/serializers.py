from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

#this is for registering new users
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'profile_picture']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            profile_picture=validated_data.get('profile_picture')
        )
        return user

#this is for retrieving user-data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'profile_picture']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                data['user'] = user  # attach the user to validated_data
                return data
            raise serializers.ValidationError("Invalid username or password")
        raise serializers.ValidationError("Must include username and password")