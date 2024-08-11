from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer



class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            
            if not serializer.is_valid(raise_exception=True):
                return Response({"message": "User creation failed", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            return Response({"message": "User creation failed", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "User creation failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid(raise_exception=True):
                return Response({"message": "Login failed", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(request.data)
           
            if(response['message']=='Invalid credentials'):
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Login failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)