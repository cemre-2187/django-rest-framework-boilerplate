from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from .serializers import BlogSerializer,CategorySerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Category
from api.core.views import BaseAPIView


class BlogView(BaseAPIView):
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
        return self.success_response(data=serializer.data, message="Blogs fetched successfully")
    
    def post(self, request):
        user = request.user
        request.data['author']=user.id
        print(request.data.user.id)
        if user.is_authenticated:
            if not int(request.data.get('author'))==int(request.user.id):
                return self.failure_response(message="You are not authorized to create a blog", status_code=status.HTTP_401_UNAUTHORIZED)
        serializer = BlogSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return self.success_response(data=serializer.data, message="Blog created successfully")
        except Exception as e:
            return self.failure_response(message="Blog creation failed", data=e.detail, status_code=status.HTTP_400_BAD_REQUEST)
    
class CategoryView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return self.success_response(data=serializer.data, message="Categories fetched successfully")
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        # check is user admin
        if not request.user.is_staff:
            return self.failure_response(message="You are not authorized to create a category", status_code=status.HTTP_401_UNAUTHORIZED)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return self.success_response(data=serializer.data, message="Category created successfully")
        except Exception as e:
            return self.failure_response(message="Category creation failed",data=e.detail , status_code=status.HTTP_400_BAD_REQUEST)