from django.urls import path, include

urlpatterns = [
    path('account/', include('api.account.urls')),
    # Assuming you have a blog application, uncomment the following line:
    # path('blog/', include('api.blog.urls')),
]
