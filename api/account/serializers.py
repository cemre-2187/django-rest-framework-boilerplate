from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, min_length=3)
    last_name = serializers.CharField(max_length=255, min_length=3)
    username = serializers.CharField(max_length=255, min_length=3)
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(write_only=True, max_length=255, min_length=6)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})
        return attrs

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user