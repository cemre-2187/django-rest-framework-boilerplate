from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from api.core.views import BaseAPIView


'''
Handles user registration by creating a new user.

Parameters:
    request (Request): The HTTP request object containing user data.

Returns:
    Response: A JSON response indicating the result of the user registration process.
'''
class RegisterView(BaseAPIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            
            if not serializer.is_valid(raise_exception=True):
                return self.error_response(message="User creation failed", status_code=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return self.success_response(message="User created successfully", status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return self.error_response(message="User creation failed", status_code=status.HTTP_400_BAD_REQUEST)
        

'''
Handles user login by authenticating the user's credentials.

Parameters:
    request (Request): The HTTP request object containing user data.

Returns:
    Response: A JSON response indicating the result of the user login process.
'''
class LoginView(BaseAPIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid(raise_exception=True):
                return self.error_response(message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(request.data)
           
            if(response['message']=='Invalid credentials'):
                return self.error_response(message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)

            return self.success_response(message="Login successful",data=response, status_code=status.HTTP_200_OK)
        except Exception as e:
            return self.error_response(message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)