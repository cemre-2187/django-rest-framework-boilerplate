from rest_framework import status  # Provides HTTP status codes for API responses
from .serializers import RegisterSerializer, LoginSerializer  # Importing serializers for user registration and login
from api.core.views import BaseAPIView  # Custom base view providing common API response methods
from drf_yasg.utils import swagger_auto_schema # Utility function for generating Swagger documentation
from drf_yasg import openapi # OpenAPI schema objects for generating Swagger documentation

'''
API view for handling user registration.
Supports creating a new user by accepting user details and saving them in the database.
'''
class RegisterView(BaseAPIView):
    @swagger_auto_schema(
        operation_summary="User registration",
        operation_description="Registers a new user by processing user-provided data.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name of the user', minLength=3, maxLength=255),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name of the user', minLength=3, maxLength=255),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for the user', minLength=3, maxLength=255),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Email address of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the user', writeOnly=True, minLength=6, maxLength=255),
            },
            required=['first_name', 'last_name', 'username', 'email', 'password'],
        ),
        responses={
            201: openapi.Response(
                description="User created successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "success")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                    }
                )
            ),
            400: openapi.Response(
                description="User creation failed due to invalid input data.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "error")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    }
                )
            ),
        }
    )
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
    @swagger_auto_schema(
        operation_summary="User login",
        operation_description="Authenticates a user based on provided username and password credentials, returning a JWT token upon successful login.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user', writeOnly=True),
            },
            required=['username', 'password'],
        ),
        responses={
            200: openapi.Response(
                description="Login successful, returns JWT token.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "success")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                                'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description="Login failed due to invalid credentials.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "error")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    }
                )
            ),
        }
    )
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