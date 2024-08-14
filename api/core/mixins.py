from rest_framework.response import Response
from rest_framework import status

class APIViewResponseMixin:
    """
    Mixin to customize the response format
    """
    
    SUCCESS = "success"
    FAILURE = "failure"

    @classmethod
    def success_response(cls, data=None, message=None, status_code=status.HTTP_200_OK):
        """
        Returns Success Response
        """
        response_data = {
          "status_code": status_code,
          "status": cls.SUCCESS
        }
        if message is not None:
            response_data["message"] = message
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status_code)

    @classmethod
    def failure_response(cls, data=None, message=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Returns Failure Response
        """
        response_data = {
          "status_code": status_code,
          "status": cls.FAILURE
        }
        if message is not None:
            response_data["message"] = message
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status_code)