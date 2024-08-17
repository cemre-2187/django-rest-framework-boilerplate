from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

'''
Serializer for registering a new user with first name, last name, username, email, and password. 
Validates if the email and username are unique. 
Creates a new User instance with the validated data and saves it to the database.
'''
class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, min_length=3)
    last_name = serializers.CharField(max_length=255, min_length=3)
    username = serializers.CharField(max_length=255, min_length=3)
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        write_only=True, max_length=255, min_length=6)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def validate(self, attrs):
        if not attrs['email'].count('@') > 0 or not attrs['email'].count('.') > 0:
            raise serializers.ValidationError(
                {"email": "Please enter a valid email address"})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "A user with this email already exists."})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {"username": "A user with this username already exists."})
   
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


'''
Serializer for user login with username and password.
Validates the username and checks if the user exists in the database.
Generates a JWT token for the authenticated user and returns it along with a success message.
'''
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Account not found')
        return attrs
        

    def get_jwt_token(self, user):
        user = authenticate(request=self.context.get('request'),
                            username=user['username'], password=user['password'])
        
        if not user:
           return {'message':'Invalid credentials'}

        refresh = RefreshToken.for_user(user)
        return {
            "message":"Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
