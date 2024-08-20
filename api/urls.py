from django.urls import path, include

urlpatterns = [
    path('account/', include('api.account.urls'), name='account'),
    path('blog/', include('api.blog.urls'), name='blog'),
]
