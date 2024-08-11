from django.urls import path, include

urlpatterns = [
    path('account/', include('api.account.urls')),
    path('blog/', include('api.blog.urls'))
]
