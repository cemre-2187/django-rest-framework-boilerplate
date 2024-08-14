
from django.db import models
from django.contrib.auth.models import User
import uuid


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
        
class Blog(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    image = models.ImageField(upload_to='blogs', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Category(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name