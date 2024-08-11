from rest_framework import serializers
from api.blog.models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['created_at', 'updated_at']
        
    def validate(self, attrs):
        return super().validate(attrs)