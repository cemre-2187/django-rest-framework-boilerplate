from django.core.cache import cache
from api.blog.models import Blog, Category
from api.blog.serializers import BlogSerializer, CategorySerializer
from rest_framework import status


class StatsService:
    @staticmethod
    def get_stats():
        # Service example
        total_blogs = Blog.objects.count()
        total_categories = Category.objects.count()
        
        return {
            "total_blogs": total_blogs,
            "total_categories": total_categories,
        }
