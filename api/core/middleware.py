import traceback
from django.utils.deprecation import MiddlewareMixin
from .models import ErrorLog
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

class LogErrorsMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        error_message = ''.join(traceback.format_exception(None, exception, exception.__traceback__))
        error_type = type(exception).__name__
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(exception, APIException):
            status_code = exception.status_code

        ErrorLog.objects.create(
            error_message=error_message,
            error_type=error_type,
            status_code=status_code,
        )

        # Custom error response
        response_data = {
            "error": error_type,
            "message": str(exception),
        }
        return Response(response_data, status=status_code)