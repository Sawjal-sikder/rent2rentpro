from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {"message": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Validation errors
    if isinstance(response.data, dict):
        for key, value in response.data.items():
            if isinstance(value, list) and value:
                return Response(
                    {"message": value[0]},
                    status=response.status_code
                )
            elif isinstance(value, str):
                return Response(
                    {"message": value},
                    status=response.status_code
                )

    return Response(
        {"message": "Something went wrong"},
        status=response.status_code
    )
