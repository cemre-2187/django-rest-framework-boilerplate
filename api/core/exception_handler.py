from rest_framework.views import exception_handler
from .models import ErrorLog

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        ErrorLog.objects.create(
            error_message=str(exc),
            error_type=type(exc).__name__,
            status_code=response.status_code,
        )

    return response