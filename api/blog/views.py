from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from .serializers import BlogSerializer
from rest_framework import status

class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        request.data['author']=user.id
        if user.is_authenticated:
            if not int(request.data.get('author'))==int(request.user.id):
                return Response({'error': 'You are not authorized to create a blog'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)