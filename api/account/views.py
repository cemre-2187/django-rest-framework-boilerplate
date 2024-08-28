from rest_framework import status  # Provides HTTP status codes for API responses
from .serializers import RegisterSerializer, LoginSerializer  # Importing serializers for user registration and login
from api.core.views import BaseAPIView  # Custom base view providing common API response methods

'''
API view for handling user registration.
Supports creating a new user by accepting user details and saving them in the database.
'''
class RegisterView(BaseAPIView):
    def post(self, request):
        '''
        Registers a new user by processing user-provided data.

        Parameters:
            request (Request): The HTTP request object containing user registration data.
        
        Returns:
            Response: A JSON response indicating the result of the user registration process.
        '''
        try:
            serializer = RegisterSerializer(data=request.data)  # Initialize the serializer with incoming registration data

            if not serializer.is_valid(raise_exception=True):
                return self.failure_response(message="User creation failed", status_code=status.HTTP_400_BAD_REQUEST)  # Return failure if data is invalid
            
            serializer.save()  # Save the new user to the database
            return self.success_response(message="User created successfully", status_code=status.HTTP_201_CREATED)  # Return success response on successful registration
        except Exception as e:
            return self.failure_response(message="User creation failed", status_code=status.HTTP_400_BAD_REQUEST)  # Handle and respond to exceptions

'''
API view for handling user login.
Validates user credentials and returns an authentication token if credentials are valid.
'''
class LoginView(BaseAPIView):
    def post(self, request):
        '''
        Authenticates a user based on provided credentials.

        Parameters:
            request (Request): The HTTP request object containing login credentials.
        
        Returns:
            Response: A JSON response indicating the result of the user login process.
        '''
        try:
            serializer = LoginSerializer(data=request.data)  # Initialize the serializer with incoming login data
            if not serializer.is_valid(raise_exception=True):
                return self.failure_response(message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)  # Return failure if data is invalid

            response = serializer.get_jwt_token(request.data)  # Get JWT token for valid credentials

            if response['message'] == 'Invalid credentials':
                return self.failure_response(message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)  # Handle invalid credentials

            return self.success_response(message="Login successful", data=response, status_code=status.HTTP_200_OK)  # Return success response with JWT token
        except Exception as e:
            return self.failure_response(message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)  # Handle and respond to exceptions