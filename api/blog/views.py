from rest_framework.permissions import IsAuthenticated  # Permission class to ensure the user is authenticated
from .models import Blog  # Importing the Blog model from the local app's models
from .serializers import BlogSerializer, CategorySerializer  # Importing serializers for Blog and Category models
from rest_framework import status  # Provides standard HTTP status codes for use in API responses
from rest_framework_simplejwt.authentication import JWTAuthentication  # JWT-based authentication class for security
from .models import Category  # Importing the Category model from the local app's models
from api.core.views import BaseAPIView  # Custom base view class for common API response methods
from django.core.cache import cache  # Django's caching framework to optimize performance
from api.core.services import StatsService  # Service class for business logic related to statistics
from drf_yasg.utils import swagger_auto_schema # Utility function for generating Swagger documentation
from drf_yasg import openapi # OpenAPI schema objects for generating Swagger documentation

'''
API view for handling operations related to blogs.
This class supports GET and POST methods for retrieving and creating blog entries.
It ensures that only authenticated users can access these functionalities.
'''
class BlogView(BaseAPIView):
    permission_classes = [IsAuthenticated]  # Restricts access to authenticated users
    authentication_classes = [JWTAuthentication]  # Utilizes JWT tokens for user authentication
    @swagger_auto_schema(
        operation_summary="Retrieve list of blog entries",
        operation_description="Retrieves a list of blog entries, optionally filtered by a search term in the title.",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Optional search term to filter blog entries by title",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description="A JSON response containing the list of blog entries.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'uid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Unique ID'),
                            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Blog title'),
                            'content': openapi.Schema(type=openapi.TYPE_STRING, description='Blog content'),
                            'author': openapi.Schema(type=openapi.TYPE_INTEGER, description='Author ID'),
                            'image': openapi.Schema(type=openapi.TYPE_STRING, description='Image URL'),
                            'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                        },
                    ),
                ),
            ),
            401: "Unauthorized - authentication credentials were not provided or are invalid."
        }
    )
    def get(self, request):
        '''
        Retrieves a list of blog entries, optionally filtered by a search term.
        
        Parameters:
            request (Request): The HTTP request object containing optional query parameters.
        
        Returns:
            Response: A JSON response containing the list of blog entries.
        '''
        search = request.query_params.get('search', None)  # Extract 'search' query parameter from request

        if search:
            blogs = Blog.objects.filter(title__icontains=search)  # Filter blogs by title using the search term
        else:
            blogs = Blog.objects.all()  # Retrieve all blog entries
        
        serializer = BlogSerializer(blogs, many=True)  # Serialize the list of blog objects
        return self.success_response(data=serializer.data, message="Blogs fetched successfully")  # Return serialized data
    @swagger_auto_schema(
        operation_summary="Create a new blog entry",
        operation_description="Creates a new blog entry for the authenticated user.",
        request_body=BlogSerializer,
        responses={
            201: openapi.Response(
                description="Blog created successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'uid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Unique ID'),
                        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Blog title'),
                        'content': openapi.Schema(type=openapi.TYPE_STRING, description='Blog content'),
                        'author': openapi.Schema(type=openapi.TYPE_INTEGER, description='Author ID'),
                        'image': openapi.Schema(type=openapi.TYPE_STRING, description='Image URL'),
                        'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                    },
                ),
            ),
            400: "Bad Request - invalid input data.",
            401: "Unauthorized - you are not authorized to create a blog."
        }
    )
    def post(self, request):
        '''
        Creates a new blog entry for the authenticated user.
        
        Parameters:
            request (Request): The HTTP request object containing blog data.
        
        Returns:
            Response: A JSON response indicating the result of the blog creation process.
        '''
        user = request.user  # Retrieve the authenticated user

        if user.is_authenticated:
            if not int(request.data.get('author')) == int(request.user.id):  # Ensure the author matches the authenticated user
                return self.failure_response(message="You are not authorized to create a blog", status_code=status.HTTP_401_UNAUTHORIZED)
        
        serializer = BlogSerializer(data=request.data)  # Create a serializer instance with incoming blog data

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()  # Save the new blog entry
                return self.success_response(data=serializer.data, message="Blog created successfully")
        except Exception as e:
            return self.failure_response(message="Blog creation failed", data=e.detail, status_code=status.HTTP_400_BAD_REQUEST)

'''
API view for managing category-related operations.
Supports GET and POST methods for retrieving and creating categories.
Implements caching to improve performance and reduce database load.
'''
class CategoryView(BaseAPIView):
    permission_classes = [IsAuthenticated]  # Restricts access to authenticated users
    authentication_classes = [JWTAuthentication]  # Utilizes JWT tokens for user authentication
    @swagger_auto_schema(
        operation_summary="Retrieve list of categories",
        operation_description="Retrieves a list of categories, with caching support to optimize performance.",
        responses={
            200: openapi.Response(
                description="A JSON response containing the list of categories.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
                        },
                    ),
                ),
            ),
            401: "Unauthorized - authentication credentials were not provided or are invalid."
        }
    )
    def get(self, request):
        '''
        Retrieves a list of categories, with caching support to optimize performance.
        
        Parameters:
            request (Request): The HTTP request object.
        
        Returns:
            Response: A JSON response containing the list of categories.
        '''
        cache_key = "categories"  # Define a cache key for storing category data
        cached_categories = cache.get(cache_key)  # Attempt to retrieve cached category data

        if cached_categories is None:
            categories = Category.objects.all()  # Retrieve all categories if no cached data
            serializer = CategorySerializer(categories, many=True)  # Serialize category data
            cache.set(cache_key, serializer.data, timeout=3600)  # Cache the serialized data for 1 hour
        else:
            serializer = CategorySerializer(cached_categories, many=True)  # Use cached data if available
        
        return self.success_response(data=serializer.data, message="Categories fetched successfully")
    @swagger_auto_schema(
        operation_summary="Create a new category",
        operation_description="Creates a new category entry, ensuring only admin users can perform this action.",
        request_body=CategorySerializer,
        responses={
            201: openapi.Response(
                description="Category created successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
                    },
                ),
            ),
            400: "Bad Request - invalid input data.",
            401: "Unauthorized - you are not authorized to create a category."
        }
    )
    def post(self, request):
        '''
        Creates a new category entry, ensuring only admin users can perform this action.
        
        Parameters:
            request (Request): The HTTP request object containing category data.
        
        Returns:
            Response: A JSON response indicating the result of the category creation process.
        '''
        serializer = CategorySerializer(data=request.data)  # Create a serializer instance with incoming category data
        cache.delete("categories")  # Invalidate the category cache

        if not request.user.is_staff:  # Check if the user is an admin
            return self.failure_response(message="You are not authorized to create a category", status_code=status.HTTP_401_UNAUTHORIZED)
        
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()  # Save the new category
                return self.success_response(data=serializer.data, message="Category created successfully")
        except Exception as e:
            return self.failure_response(message="Category creation failed", data=e.detail, status_code=status.HTTP_400_BAD_REQUEST)

'''
API view for handling statistics-related operations.
This view allows retrieving various statistics, accessible only to authenticated users.
'''
class StatsView(BaseAPIView):
    permission_classes = [IsAuthenticated]  # Restricts access to authenticated users
    authentication_classes = [JWTAuthentication]  # Utilizes JWT tokens for user authentication
    @swagger_auto_schema(
        operation_summary="Retrieve statistical data",
        operation_description="Retrieves statistical data related to the application, including total blogs and total categories.",
        responses={
            200: openapi.Response(
                description="A JSON response containing statistical data.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_blogs': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of blogs'),
                        'total_categories': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of categories'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                    },
                ),
            ),
            401: "Unauthorized - authentication credentials were not provided or are invalid."
        }
    )
    def get(self, request):
        '''
        Retrieves statistical data related to the application.
        
        Parameters:
            request (Request): The HTTP request object.
        
        Returns:
            Response: A JSON response containing statistical data.
        '''
        stats = StatsService.get_stats()  # Retrieve statistics using the StatsService
        return self.success_response(data=stats, message="Stats fetched successfully")