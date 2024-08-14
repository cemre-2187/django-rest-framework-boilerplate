from rest_framework.views import APIView
from api.core.mixins import APIViewResponseMixin

class BaseAPIView(APIView, APIViewResponseMixin):
    """
    Create a base API view that combines APIView and APIViewResponseMixin
    Custom API View to handle all the common logic for all APIs
    """  
    def get_authenticate_header(self, request):
        return super().get_authenticate_header(request)
    pass