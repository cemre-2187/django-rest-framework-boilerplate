from rest_framework.views import APIView
from api.core.mixins import APIViewResponseMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class BaseAPIView(APIView, APIViewResponseMixin):
    """
    Custom base API view to handle common logic for all APIs.
    """
    # Add custom middleware logic to here for all API views
    def dispatch(self, request, *args, **kwargs):
        # Custom middleware logic can be added here
        print("Custom middleware logic for all API views If you need it", "/api/core/views.py")
        return super().dispatch(request, *args, **kwargs)
    
    pass