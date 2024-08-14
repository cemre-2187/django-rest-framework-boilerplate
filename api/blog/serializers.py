from rest_framework import serializers
from api.blog.models import Blog, Category

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['created_at', 'updated_at']
    
        
    def validate(self, attrs):
        return super().validate(attrs)
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['created_at', 'updated_at']
    
    def validate(self, attrs):
        return super().validate(attrs)