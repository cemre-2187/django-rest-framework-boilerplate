import traceback
from django.utils.deprecation import MiddlewareMixin
from .models import ErrorLog
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.conf import settings

class LogErrorsMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print('exception', exception)
        error_message = exception.__str__()
        error_type = type(exception).__name__
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
       
        if isinstance(exception, APIException):
            status_code = exception.status_code

        ErrorLog.objects.create(
            error_message=error_message,
            error_type=error_type,
            status_code=status_code,
        )
        # If it is DEBUG mode, return the exception. If not return a generic error message
        if settings.DEBUG:
            response_data = {
            "status_code": status_code,
            "error": error_type,
            "message": str(exception),
             }
            return JsonResponse(response_data, status=status_code)
        else:
            response_data = {
            "status_code": status_code,
            "error": "Unexpected Error",
            "message": "An unexpected error occurred. Please try again later.",
             }
            return JsonResponse(response_data, status=status_code)
      