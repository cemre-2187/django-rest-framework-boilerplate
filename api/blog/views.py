from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from .serializers import BlogSerializer,CategorySerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Category


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        #add search query
        search = request.query_params.get('search', None)
        if search:
            blogs = Blog.objects.filter(title__icontains=search)
        else:
            blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        request.data['author']=user.id
        print(request.data.user.id)
        if user.is_authenticated:
            if not int(request.data.get('author'))==int(request.user.id):
                return Response({'error': 'You are not authorized to create a blog'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        # check is user admin
        if not request.user.is_staff:
            return Response({'error': 'You are not authorized to create a category'}, status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)