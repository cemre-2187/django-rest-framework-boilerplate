# Permission class to ensure the user is authenticated
from rest_framework.permissions import IsAuthenticated
from .models import Blog  # Importing the Blog model from the local app's models
# Importing serializers for Blog and Category models
from .serializers import BlogSerializer, CategorySerializer
# Provides standard HTTP status codes for use in API responses
from rest_framework import status
# JWT-based authentication class for security
from rest_framework_simplejwt.authentication import JWTAuthentication
# Importing the Category model from the local app's models
from .models import Category
# Custom base view class for common API response methods
from api.core.views import BaseAPIView
# Django's caching framework to optimize performance
from django.core.cache import cache
# Service class for business logic related to statistics
from api.core.services import StatsService
# Utility function for generating Swagger documentation
from drf_yasg.utils import swagger_auto_schema
# OpenAPI schema objects for generating Swagger documentation
from drf_yasg import openapi

'''
API view for handling operations related to blogs.
This class supports GET and POST methods for retrieving and creating blog entries.
It ensures that only authenticated users can access these functionalities.
'''


class BlogView(BaseAPIView):
    # Restricts access to authenticated users
    permission_classes = [IsAuthenticated]
    # Utilizes JWT tokens for user authentication
    authentication_classes = [JWTAuthentication]

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
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "success")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                        'data': openapi.Schema(
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
                                }
                            )
                        ),
                    }
                )
            ),
            401: openapi.Response(
                description="Unauthorized - authentication credentials were not provided or are invalid.",
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
    def get(self, request):
        '''
        Retrieves a list of blog entries, optionally filtered by a search term.

        Parameters:
            request (Request): The HTTP request object containing optional query parameters.

        Returns:
            Response: A JSON response containing the list of blog entries.
        '''
        search = request.query_params.get(
            'search', None)  # Extract 'search' query parameter from request

        if search:
            # Filter blogs by title using the search term
            blogs = Blog.objects.filter(title__icontains=search)
        else:
            blogs = Blog.objects.all()  # Retrieve all blog entries

        # Serialize the list of blog objects
        serializer = BlogSerializer(blogs, many=True)
        # Return serialized data
        return self.success_response(data=serializer.data, message="Blogs fetched successfully")

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
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "success")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'uid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Unique ID'),
                                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Blog title'),
                                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Blog content'),
                                'author': openapi.Schema(type=openapi.TYPE_INTEGER, description='Author ID'),
                                'image': openapi.Schema(type=openapi.TYPE_STRING, description='Image URL'),
                                'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request - invalid input data.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "error")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    }
                )
            ),
            401: openapi.Response(
                description="Unauthorized - you are not authorized to create a blog.",
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
        Creates a new blog entry for the authenticated user.

        Parameters:
            request (Request): The HTTP request object containing blog data.

        Returns:
            Response: A JSON response indicating the result of the blog creation process.
        '''
        user = request.user  # Retrieve the authenticated user

        if user.is_authenticated:
            # Ensure the author matches the authenticated user
            if not int(request.data.get('author')) == int(request.user.id):
                return self.failure_response(message="You are not authorized to create a blog", status_code=status.HTTP_401_UNAUTHORIZED)

        # Create a serializer instance with incoming blog data
        serializer = BlogSerializer(data=request.data)

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
    # Restricts access to authenticated users
    permission_classes = [IsAuthenticated]
    # Utilizes JWT tokens for user authentication
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_summary="Retrieve list of categories",
        operation_description="Retrieves a list of categories, with caching support to optimize performance.",
        responses={
            200: openapi.Response(
                description="A JSON response containing the list of categories.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "success")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
                                }
                            )
                        ),
                    }
                )
            ),
            401: openapi.Response(
                description="Unauthorized - authentication credentials were not provided or are invalid.",
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
    def get(self, request):
        '''
        Retrieves a list of categories, with caching support to optimize performance.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing the list of categories.
        '''
        cache_key = "categories"  # Define a cache key for storing category data
        # Attempt to retrieve cached category data
        cached_categories = cache.get(cache_key)

        if cached_categories is None:
            categories = Category.objects.all()  # Retrieve all categories if no cached data
            serializer = CategorySerializer(
                categories, many=True)  # Serialize category data
            # Cache the serialized data for 1 hour
            cache.set(cache_key, serializer.data, timeout=3600)
        else:
            # Use cached data if available
            serializer = CategorySerializer(cached_categories, many=True)

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
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "success")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request - invalid input data.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "error")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    }
                )
            ),
            401: openapi.Response(
                description="Unauthorized - you are not authorized to create a category.",
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
        Creates a new category entry, ensuring only admin users can perform this action.

        Parameters:
            request (Request): The HTTP request object containing category data.

        Returns:
            Response: A JSON response indicating the result of the category creation process.
        '''
        serializer = CategorySerializer(
            data=request.data)  # Create a serializer instance with incoming category data
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
    # Restricts access to authenticated users
    permission_classes = [IsAuthenticated]
    # Utilizes JWT tokens for user authentication
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_summary="Retrieve application statistics",
        operation_description="Retrieves statistical data related to the application.",
        responses={
            200: openapi.Response(
                description="A JSON response containing statistical data.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the response (e.g., "success")'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'total_blogs': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of blogs'),
                                'total_categories': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of categories'),
                            }
                        ),
                    }
                )
            ),
            401: openapi.Response(
                description="Unauthorized - authentication credentials were not provided or are invalid.",
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
