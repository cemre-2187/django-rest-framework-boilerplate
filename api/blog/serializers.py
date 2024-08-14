from rest_framework import serializers
from api.blog.models import Blog, Category

class CategoryField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            return Category.objects.get(name=data)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category with this name does not exist.")

class BlogSerializer(serializers.ModelSerializer):
    category = CategoryField(queryset=Category.objects.all())
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